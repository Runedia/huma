"""
영화사 목록 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchCompanyList)

최초 작성일: 2021-09-30
작성자: 김태희
버전: 1.0.1

변경이력
- 2021-09-30 | 1.0.0 | 김태희 | 최초작성
- 2021-10-01 | 1.0.1 | 김태희 | 구조 변경 및 DB 중복 제어

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
import math
from cf import API_KEY, COMPANY_LIST
from DBMTool import conn


def get_company_list_url(curPage=1, itemPerPage=100):
    """
    영화사 목록을 가져오는 URL 생성 함수

    Args:
        curPage (int): 현재 페이지
        itemPerPage (int): 페이지당 항목 수

    Returns:
        str: 영화사 목록 REST API URL
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json'
    params = {
        'key': API_KEY,
        'curPage': curPage,
        'itemPerPage': itemPerPage,
    }

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_company_list_request(url):
    """
    영화사 목록을 조회하는 함수
    """

    print(f'REQUEST URL (COMPANY LIST): {url}')
    # 데이터를 가져올 Request 객체 생성
    req = urllib.request.Request(url)

    try:
        # 데이터 조회
        response = urllib.request.urlopen(req)

        # Http Code가 200일 경우 통신 성공
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None


def duplication_check_company_list(companyCd):
    """
    companylist 테이블에 조회하여 영화사코드 중복여부를 확인

    Returns:
        bool: 중복여부
    """

    result = conn.execute(f"SELECT COUNT(*) FROM {COMPANY_LIST} WHERE companyCd = '{companyCd}'").fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])


def get_company_list():
    """
    영화사 목록 데이터를 정제하여 DB에 저장하는 함수
    """

    curPage = 1
    itemPerPage = 100
    maxPage = 1

    while True:
        url = get_company_list_url(curPage, itemPerPage)
        response = get_company_list_request(url)

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json?key=eec39ee4692d829911723511a238286d&companyNm=%EA%B8%88%EC%84%B1
            response_json = json.loads(response)
            totCnt = response_json['companyListResult']['totCnt']
            maxPage = math.ceil(totCnt / itemPerPage)

            # companyListResult에 포함되어 있는 companyList
            df_comlist = pd.DataFrame(response_json['companyListResult']['companyList'])
            # 영화사 데이터 filmoNames 삭제
            df_comlist = df_comlist.drop(columns='filmoNames')

            # 영화 목록 중복 제어
            temp_ary = []

            for index, row in df_comlist.iterrows():
                if not duplication_check_company_list(row['companyCd']):
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
