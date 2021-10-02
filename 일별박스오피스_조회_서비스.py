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
from cf import API_KEY, BOXOFFICE_LIST
from DBMTool import conn

# START_DAYS = datetime.datetime(2010, 1, 1)
START_DAYS = datetime.datetime(2011, 9, 26)
END_DAYS = datetime.datetime.now() - datetime.timedelta(days=1)


def get_boxoffice_list_url(targetDt):
    """
    박스오피스 목록을 가져오는 URL 생성 함수

    Args:
        curPage (int): 현재 페이지
        itemPerPage (int): 페이지당 항목 수

    Returns:
        str: 박스오피스 목록 REST API URL
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    params = {
        'key': API_KEY,
        'targetDt': targetDt,
        'repNationCd': 'K',
    }

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_boxoffice_list_request(url):
    """
    박스오피스 목록을 조회하는 함수
    """

    print(f'REQUEST URL (BOXOFFICE) LIST): {url}')
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


def duplication_check_boxoffice_list(movieCd, targetDt):
    """
    boxoffice 테이블에 조회하여 영화코드 중복여부를 확인한다.

    Returns:
        bool: 중복여부
    """

    result = conn.execute(f"SELECT COUNT(*) FROM {BOXOFFICE_LIST} WHERE movieCd = '{movieCd}' AND targetDt = '{targetDt}'").fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])


def get_boxoffice_list():
    """
    박스오피스 데이터를 정제하여 DB에 저장하는 함수
    """

    posDt = START_DAYS

    while True:
        targetDt = posDt.strftime('%Y%m%d')
        url = get_boxoffice_list_url(targetDt)
        response = get_boxoffice_list_request(url)

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시

            response_json = json.loads(response)

            df_boxofficelist = pd.DataFrame(response_json['boxOfficeResult']['dailyBoxOfficeList'])
            df_boxofficelist['targetDt'] = targetDt
            
            temp_open_dt = []
            for idx, row in df_boxofficelist['openDt'].iteritems():
                openDt = row
                if str(openDt).strip():
                    temp_open_dt.append(openDt)
                else:
                    temp_open_dt.append(None)

            df_boxofficelist['openDt'] = temp_open_dt

            # 영화 목록 중복 제어
            temp_ary = []

            for index, row in df_boxofficelist.iterrows():
                if not duplication_check_boxoffice_list(row['movieCd'], targetDt):
                    temp_ary.append(row)

            if len(temp_ary):
                df_temp = pd.DataFrame(temp_ary)

                # print(df_temp.to_string())

                # database에 조회한 영화목록 저장
                # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
                df_temp.to_sql(BOXOFFICE_LIST, conn, index=False, if_exists='append')

        if posDt == END_DAYS:
            print('박스오피스 목록 Collecting 완료')
            break

        posDt += datetime.timedelta(days=1)


if __name__ == '__main__':
    get_boxoffice_list()
