"""
영화목록 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchMovieList)

최초 작성일: 2021-09-30
작성자: 김지호
버전: 1.0.2

변경이력
- 2021-09-30 | 1.0.0 | 김지호 | 최초작성
- 2021-10-01 | 1.0.1 | 김지호 | 구조 변경 및 DB 중복 제어
- 2021-10-03 | 1.0.2 | 김지호 | 구조 변경 및 주석 추가

영화 목록 조회 조건
기간: 2010 ~
장르: 장편
국가: 한국
"""

import math

import pandas as pd

from API_Common import get_api_url, get_api_request, duplication_check_code
from DBMTool import conn
from cf import API_KEY, MOVIE_LIST


def get_movie_list():
    """
    영화 목록 데이터를 정제하여 DB에 저장하는 함수
    """

    # 영화 목록 baseURL
    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'

    # 현재 페이지
    curPage = 1
    # 페이지당 항목 수
    itemPerPage = 100
    # 마지막 페이지
    maxPage = 1

    while True:
        params = {
            'key': API_KEY,
            'curPage': curPage,
            'itemPerPage': itemPerPage,
            'prdtStartYear': '2010',
            'prdtEndYear': '2021',
            # 국가코드 (한국)
            # repNationCd (http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml?key={API_KEY}&comCode=2204)
            'repNationCd': '22041011',
            # 영화 장르 (장편, 단편, 옵니버스, 기타)
            # movieTypeCd (http://kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml?key={API_KEY}&comCode=2201)
            'movieTypeCd': '220101',
        }
        url = get_api_url(baseURL, params)
        response = get_api_request(url, "MOVIE LIST")

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=f5eef3421c602c6cb7ea224104795888&movieNm=%EB%B3%B4%EC%9D%B4%EC%8A%A4

            # API 조회 시 totCnt라는 항목에 최대 갯수를 반환해준다.
            # itemPerPage를 기준으로 계산하여 마지막 페이지를 계산한다.
            totCnt = response['movieListResult']['totCnt']
            maxPage = math.ceil(totCnt / itemPerPage)

            df_mvlist = pd.DataFrame(response['movieListResult']['movieList'])
            # 영화 상세정보가 더 명확하게 표출되어 데이터 삭제
            df_mvlist = df_mvlist.drop(columns='directors')  # 영화감독
            df_mvlist = df_mvlist.drop(columns='companys')  # 제작사

            # 영화 목록 중복 제어
            temp_ary = []

            for index, row in df_mvlist.iterrows():
                sql = f"SELECT COUNT(*) FROM {MOVIE_LIST} WHERE movieCd = '{row['movieCd']}'"
                if not duplication_check_code(conn, sql):
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
