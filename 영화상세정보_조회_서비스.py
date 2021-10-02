"""
영화상세 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchMovieInfo)

최초 작성일: 2021-10-01
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-10-01 | 1.0.0 | 김지호 | 최초작성

<개발 순서>
1. DB 연결
2. REST API 조회
3. REST API 가공
4. DATA 저장
5. 오류제어
"""

from urllib.parse import urlparse, urlunparse, urlencode
import urllib.request
import json
import pandas as pd
import datetime
from cf import API_KEY, MOVIE_LIST, MOVIE_INFO
from DBMTool import conn


def get_movie_info_url(movieCd):
    """
    영화 상세 정보를 가져오는 URL 생성 함수

    Args:
        movieCd (str): 영화코드

    Returns:
        str: 영화 상세 정보 REST API URL
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    params = {
        'key': API_KEY,
        'movieCd': movieCd
    }

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_movie_info_request(url):
    """
    영화 상세 정보를 조회하는 함수
    """

    print(f'REQUEST URL (MOVIE INFO): {url}')
    # 데이터를 가져올 Request 객체를 생성한다.
    req = urllib.request.Request(url)

    try:
        # 데이터를 조회한다.
        response = urllib.request.urlopen(req)

        # Http Code가 200일 경우 통신 성공
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None


def get_movie_code_list():
    result = conn.execute(f"""
        SELECT 
            ml.movieCd
        FROM
            {MOVIE_LIST} AS ml
                LEFT JOIN
            {MOVIE_INFO} AS mi ON ml.movieCd = mi.movieCd
        WHERE
            mi.movieCd IS NULL
    """).fetchall()

    if result is None:
        return None
    else:
        return result


def duplication_check_movie_info(movieCd):
    """
    MOVIE_INFO 테이블에 조회하여 영화코드 중복여부를 확인한다.

    Returns:
        bool: 중복여부
    """

    result = conn.execute(f"SELECT COUNT(*) FROM {MOVIE_INFO} WHERE movieCd = '{movieCd}'").fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])


def get_movie_info():
    """
    영화 상세 정보 데이터를 정제하여 DB에 저장하는 함수
    """

    movieCds = get_movie_code_list()

    for data in movieCds:
        movieCd = data[0]

        url = get_movie_info_url(movieCd)
        response = get_movie_info_request(url)

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml?key=f5eef3421c602c6cb7ea224104795888&movieCd=20190815
            response_json = json.loads(response)
            df_mvinfo = pd.DataFrame([response_json['movieInfoResult']['movieInfo']])
            df_mvinfo = df_mvinfo.drop(columns='staffs')  # 스텝
            df_mvinfo = df_mvinfo.drop(columns='showTypes')  # 상영형태
            df_mvinfo['showTm'] = df_mvinfo['showTm'].fillna(0, inplace=True)

            for idx, row in df_mvinfo.iterrows():
                # 감독
                nations = ",".join([nat['nationNm'] for nat in row['nations']])
                row['nations'] = nations

                # 장르
                genres = ",".join([nat['genreNm'] for nat in row['genres']])
                row['genres'] = genres

                # 감독 (임시) 추후 영화인 정보와 연동
                directors = ",".join([nat['peopleNm'] for nat in row['directors']])
                row['directors'] = directors

                # 배우 (임시) 추후 영화인 정보와 연동
                actors = ",".join([nat['peopleNm'] for nat in row['actors'] if str(nat['peopleNmEn']).strip()])
                row['actors'] = actors

                # 회사 (임시) 추후 영화사 정보와 연동
                companys = ",".join([nat['companyCd'] for nat in row['companys']])
                row['companys'] = companys

                # 심의정보
                audits = ",".join([nat['watchGradeNm'] for nat in row['audits']])
                row['audits'] = audits

            # 영화 목록 중복 제어
            temp_ary = []

            for index, row in df_mvinfo.iterrows():
                if not duplication_check_movie_info(movieCd):
                    temp_ary.append(row)

            if len(temp_ary):
                df_temp = pd.DataFrame(temp_ary)

                # print(df_temp.to_string())

                # database에 조회한 영화목록 저장
                # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
                df_temp.to_sql(MOVIE_INFO, conn, index=False, if_exists='append')


if __name__ == '__main__':
    get_movie_info()
