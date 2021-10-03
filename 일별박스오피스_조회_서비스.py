"""
박스오피스 조회 서비스
(http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do)

최초 작성일: 2021-10-01
작성자: 김태희
버전: 1.0.1

변경이력
- 2021-10-01 | 1.0.0 | 김태희 | 최초작성
- 2021-10-03 | 1.0.1 | 김지호 | 구조 변경 및 주석 추가
"""

import datetime

import pandas as pd

from API_Common import get_api_url, get_api_request, duplication_check_code
from DBMTool import conn
from cf import API_KEY, BOXOFFICE_LIST

# 조회 시작일
START_DAYS = datetime.date(2010, 1, 1)

# 조회 종료일
END_DAYS = datetime.date.today() - datetime.timedelta(days=1)


def get_boxoffice_list():
    """
    박스오피스 데이터를 정제하여 DB에 저장하는 함수
    """

    # 박스오피스 baseURL
    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'

    posDt = START_DAYS

    while True:
        targetDt = posDt.strftime('%Y%m%d')
        params = {
            'key': API_KEY,
            'targetDt': targetDt,
            'repNationCd': 'K',
        }

        url = get_api_url(baseURL, params)
        response = get_api_request(url, "BOXOFFICE LIST")

        if response is None:  # 오류일 경우 패스 (오류무시)
            pass
        else:
            # JSON 구조 예시
            # http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=f5eef3421c602c6cb7ea224104795888&targetDt=20120101

            df_boxofficelist = pd.DataFrame(response['boxOfficeResult']['dailyBoxOfficeList'])
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
                sql = f"SELECT COUNT(*) FROM {BOXOFFICE_LIST} WHERE movieCd = '{row['movieCd']}' AND targetDt = '{targetDt}'"
                if not duplication_check_code(conn, sql):
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
