"""
영화목록 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do)

최초 작성일: 2021-09-30
작성자: 김지호
버전: 1.0.1

변경이력
- 2021-09-30 | 1.0.0 | 김지호 | 최초작성
- 2021-10-01 | 1.0.1 | 김지호 | 구조 변경 및 DB 중복 제어

<개발 순서>
1. DB 연결
2. REST API 조회
3. REST API 가공
4. DATA 저장
5. 오류제어

영화 목록 조회 조건
기간: 2010 ~
장르: 장편
국가: 한국
"""

from urllib.parse import urlparse, urlunparse, urlencode
import urllib.request
import json
import pandas as pd
import datetime
import math
from cf import API_KEY, KOREA, FEATURE, MOVIE_LIST
from DBMTool import conn


def get_movie_list_url(curPage=1, itemPerPage=100):
    """
    영화 목록을 가져오는 URL 생성 함수

    Args:
        curPage (int): 현재 페이지
        itemPerPage (int): 페이지당 항목 수

    Returns:
        str: 영화 목록 REST API URL
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    params = {
        'key': API_KEY,
        'curPage': curPage,
        'itemPerPage': itemPerPage,
        'prdtStartYear': '2010',
        'prdtEndYear': '2021',
        'repNationCd': KOREA,
        'movieTypeCd': FEATURE,
    }
    # openStartDt과 openEndDt은 재개봉이 포함이 된다.

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_movie_list_request(url):
    """
    영화 목록을 조회하는 함수
    """

    print(f'REQUEST URL (MOVIE LIST): {url}')
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


def duplication_check_movie_list(movieCd):
    result = conn.execute(f"SELECT COUNT(*) FROM {MOVIE_LIST} WHERE movieCd = '{movieCd}'").fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])


def get_movie_list():
    """
    영화 목록을 정제하여 DB에 저장하는 함수
    """

    curPage = 1
    itemPerPage = 100
    maxPage = curPage + 0

    while True:
        url = get_movie_list_url(curPage, itemPerPage)
        response = get_movie_list_request(url)

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            response_json = json.loads(response)
            totCnt = response_json['movieListResult']['totCnt']
            maxPage = math.ceil(totCnt / itemPerPage)

            df_mvlist = pd.DataFrame(response_json['movieListResult']['movieList'])
            # 영화 상세정보가 더 명확하게 표출되어 데이터 삭제
            df_mvlist = df_mvlist.drop(columns='directors')  # 영화감독
            df_mvlist = df_mvlist.drop(columns='companys')  # 제작사

            # 영화 목록 중복 제어
            temp_ary = []

            for index, row in df_mvlist.iterrows():
                if not duplication_check_movie_list(row['movieCd']):
                    temp_ary.append(row)

            if len(temp_ary):
                df_temp = pd.DataFrame(temp_ary)

                # print(df_temp.to_string())

                # database에 조회한 영화목록 저장
                # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
                df_temp.to_sql(MOVIE_LIST, conn, index=False, if_exists='append')

        if curPage == maxPage:
            print('영화 목록 Collecting 완료')
            break

        curPage += 1


if __name__ == '__main__':
    get_movie_list()
