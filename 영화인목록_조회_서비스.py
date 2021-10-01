"""
영화인 목록 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchPeopleList)

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
from cf import API_KEY, PEOPLE_LIST
from DBMTool import conn


def get_people_list_url(curPage=1, itemPerPage=100):
    """
    영화인 목록을 가져오는 URL 생성 함수

    Args:
        curPage (int): 현재 페이지
        itemPerPage (int): 페이지당 항목 수

    Returns:
        str: 영화인 목록 REST API URL
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
    params = {
        'key': API_KEY,
        'curPage': curPage,
        'itemPerPage': itemPerPage,
    }

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_people_list_request(url):
    """
    영화인 목록을 조회하는 함수
    """

    print(f'REQUEST URL (PEOPLE LIST): {url}')
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


def duplication_check_people_list(peopleCd):
    """
    peoplelist 테이블에 조회하여 영화인코드 중복여부를 확인한다.

    Returns:
        bool: 중복여부
    """

    result = conn.execute(f"SELECT COUNT(*) FROM {PEOPLE_LIST} WHERE peopleCd = '{peopleCd}'").fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])


def get_people_list():
    """
    영화인 목록 데이터를 정제하여 DB에 저장하는 함수
    """

    curPage = 1
    itemPerPage = 100
    maxPage = 1

    while True:
        url = get_people_list_url(curPage, itemPerPage)
        response = get_people_list_request(url)

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=eec39ee4692d829911723511a238286d&peopleNm=%EC%9D%B4%EC%A0%95%EC%9E%AC
            response_json = json.loads(response)
            totCnt = response_json['peopleListResult']['totCnt']
            maxPage = math.ceil(totCnt / itemPerPage)

            df_ppllist = pd.DataFrame(response_json['peopleListResult']['peopleList'])
            # df_ppllist = df_ppllist.drop(columns='filmoNames')

            # 영화인 목록 중복 제어
            temp_ary = []

            for index, row in df_ppllist.iterrows():
                if not duplication_check_people_list(row['peopleCd']):
                    temp_ary.append(row)

            if len(temp_ary):
                df_temp = pd.DataFrame(temp_ary)

                # print(df_temp.to_string())

                # database에 조회한 영화인목록 저장
                # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
                df_temp.to_sql(PEOPLE_LIST, conn, index=False, if_exists='append')

        if curPage == maxPage:
            print('영화인 목록 Collecting 완료')
            break

        curPage += 1


if __name__ == '__main__':
    get_people_list()
