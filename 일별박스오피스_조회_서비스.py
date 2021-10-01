"""
박스오피스 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do)

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
from cf import API_KEY, BOXOFFICE_LIST
from DBMTool import conn


def get_boxoffice_list_url(curPage=1, itemPerPage=10):
    """
    영화 목록을 가져오는 URL 생성 함수

    Args:
        curPage (int): 현재 페이지
        itemPerPage (int): 페이지당 항목 수

    Returns:
        str: 영화 목록 REST API URL
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    params = {
        'key': API_KEY,
        'targetDt' : 
        'curPage': curPage,
        'itemPerPage': itemPerPage,
        'repNationCd': 'K',
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
    """
    MOVIE_LIST 테이블에 조회하여 영화코드 중복여부를 확인한다.

    Returns:
        bool: 중복여부
    """

    result = conn.execute(f"SELECT COUNT(*) FROM {MOVIE_LIST} WHERE movieCd = '{movieCd}'").fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])


def get_movie_list():
    """
    영화 목록 데이터를 정제하여 DB에 저장하는 함수
    """

    curPage = 1
    itemPerPage = 100
    maxPage = 1

    while True:
        url = get_movie_list_url(curPage, itemPerPage)
        response = get_movie_list_request(url)

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=f5eef3421c602c6cb7ea224104795888&movieNm=%EB%B3%B4%EC%9D%B4%EC%8A%A4
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
