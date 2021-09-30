"""
2021-09-30

필요 라이브러리
- pip install pymysql
- pip install sqlalchemy
- pip install pandas

1. DB 접속



"""
import pymysql
from sqlalchemy import create_engine
from urllib.parse import urlparse, urlunparse, urlencode
import urllib.request
import json
import pandas as pd

API_KEY = '5ae88f21ef91305b8eb978447797ee72'


def db_conn():
    # 데이터베이스 접속을 위해 사전 실행하는 코드
    pymysql.install_as_MySQLdb()

    # DB 정보 구성
    DB_HOST = 'runedia.kro.kr'
    DB_PORT = '6033'
    DB_USERNAME = 'huma'
    DB_PASSWORD = 'huma2021^'
    DB_URL = f'mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/huma'
    print(f'DB_URL: {DB_URL}')

    # DB 연결 설정
    engine = create_engine(DB_URL, encoding='utf8', echo=False)

    # DB 연결
    conn = engine.connect()

    # result = conn.execute('SELECT * FROM movielist;').fetchall()
    # print(result)

    return conn


def get_movie_list_url():
    """
    영화 목록을 가져오는 URL 생성 함수
    """

    baseURL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    params = {
        'key': API_KEY,
        'curPage': 1,
        'itemPerPage': 100,
        'prdtStartYear': '2010',
        'prdtEndYear': '2020',
    }
    # openStartDt과 openEndDt은 재개봉이 포함이 된다.

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_movie_list_request(url):
    """
    영화 목록을 조회하는 함수
    """

    print(f'REQUEST URL: {url}')
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


def get_movie_list(conn):
    """
    영화 목록을 정제하여 DB에 저장하는 함수
    """

    url = get_movie_list_url()
    response = get_movie_list_request(url)

    if response is None:  # 오류일 경우 패스 (오류무시)
        pass
    else:
        response_json = json.loads(response)
        totCnt = response_json['movieListResult']['totCnt']
        df_mvlist = pd.DataFrame(response_json['movieListResult']['movieList'])
        # 임시 제거 시작
        df_mvlist = df_mvlist.drop('directors', 1) 
        df_mvlist = df_mvlist.drop('companys', 1)
        # 임시 제거 종료
        
        # print(df_mvlist)

        # database에 조회한 영화목록 저장
        # (테이블명, 엔진, 인덱스 생성 여부, 넣는 방법)
        df_mvlist.to_sql('movielist', conn, index=False, if_exists='append')


def main():
    print('\n\n')
    conn = db_conn()
    get_movie_list(conn)

    print('\n\n')


main()
