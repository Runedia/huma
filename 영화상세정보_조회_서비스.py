"""
영화상세 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchMovieInfo)

최초 작성일: 2021-10-01
작성자: 김지호
버전: 1.0.1

변경이력
- 2021-10-01 | 1.0.0 | 김지호 | 최초작성
- 2021-10-03 | 1.0.1 | 김지호 | 구조 변경 및 주석 추가
"""

import pandas as pd

from API_Common import get_api_url, get_api_request, duplication_check_code
from DBMTool import conn
from cf import API_KEY, MOVIE_LIST, MOVIE_INFO


def get_movie_code_list():
    """
    영화정보가 수집되지 않은 영화코드 목록

    Returns:
        list: 영화코드 목록
    """
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


def get_movie_info():
    """
    영화 상세 정보 데이터를 정제하여 DB에 저장하는 함수
    """

    # 영화 코드 목록
    movieCds = get_movie_code_list()

    # 영화 상세 정보 baseURL
    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

    for data in movieCds:
        movieCd = data[0]
        params = {
            'key': API_KEY,
            'movieCd': movieCd
        }

        url = get_api_url(baseURL, params)
        response = get_api_request(url, "MOVIE INFO")

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml?key=f5eef3421c602c6cb7ea224104795888&movieCd=20190815

            df_mvinfo = pd.DataFrame([response['movieInfoResult']['movieInfo']])
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
                # 일반적으로 인물정보 조회가 가능한 배우만 영문명이 기록되어 있음
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
                sql = f"SELECT COUNT(*) FROM {MOVIE_INFO} WHERE movieCd = '{movieCd}'"
                if not duplication_check_code(conn, sql):
                    temp_ary.append(row)

            if len(temp_ary):
                df_temp = pd.DataFrame(temp_ary)

                # print(df_temp.to_string())

                # database에 조회한 영화목록 저장
                # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
                df_temp.to_sql(MOVIE_INFO, conn, index=False, if_exists='append')


if __name__ == '__main__':
    get_movie_info()
