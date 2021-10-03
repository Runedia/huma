"""
영화사 목록 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchCompanyList)

최초 작성일: 2021-09-30
작성자: 김태희
버전: 1.0.2

변경이력
- 2021-09-30 | 1.0.0 | 김태희 | 최초작성
- 2021-10-01 | 1.0.1 | 김태희 | 구조 변경 및 DB 중복 제어
- 2021-10-03 | 1.0.2 | 김지호 | 구조 변경 및 주석 추가
"""

import math

import pandas as pd

from API_Common import get_api_url, get_api_request, duplication_check_code
from DBMTool import conn
from cf import API_KEY, COMPANY_LIST


def get_company_list():
    """
    영화사 목록 데이터를 정제하여 DB에 저장하는 함수
    """

    # 영화사 목록 baseURL
    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json'

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
        }
        url = get_api_url(baseURL, params)
        response = get_api_request(url, "COMPANY LIST")

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json?key=eec39ee4692d829911723511a238286d&companyNm=%EA%B8%88%EC%84%B1

            # API 조회 시 totCnt라는 항목에 최대 갯수를 반환해준다.
            # itemPerPage를 기준으로 계산하여 마지막 페이지를 계산한다.
            totCnt = response['companyListResult']['totCnt']
            maxPage = math.ceil(totCnt / itemPerPage)

            # companyListResult에 포함되어 있는 companyList
            df_comlist = pd.DataFrame(response['companyListResult']['companyList'])
            # 영화사 데이터 filmoNames 삭제
            df_comlist = df_comlist.drop(columns='filmoNames')

            # 영화사 목록 중복 제어
            temp_ary = []

            for index, row in df_comlist.iterrows():
                sql = f"SELECT COUNT(*) FROM {COMPANY_LIST} WHERE companyCd = '{row['companyCd']}'"
                if not duplication_check_code(conn, sql):
                    temp_ary.append(row)

            if len(temp_ary):
                df_temp = pd.DataFrame(temp_ary)

                # print(df_temp.to_string())

                # database에 조회한 영화목록 저장
                # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
                df_temp.to_sql(COMPANY_LIST, conn, index=False, if_exists='append')

        if curPage == maxPage:
            print('영화사 목록 Collecting 완료')
            break

        curPage += 1


# 다른 곳에서 불러올때 계속 실행안되게 방지하는 용도
if __name__ == '__main__':
    get_company_list()
