"""
API에서 공통적으로 사용하는 함수를 관리한다.

최초 작성일: 2021-10-03
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-10-03 | 1.0.0 | 김지호 | 최초작성
"""
import json
from urllib import request as request
from urllib.parse import urlparse, urlunparse, urlencode


def get_api_url(baseURL, params):
    """
    API URL 생성 함수

    Args:
        baseURL (str): API URL
        params (dict): 파라미터

    Returns:
        str: REST API URL
    """

    url = urlparse(baseURL)
    url = url._replace(query=urlencode(params))
    return urlunparse(url)


def get_api_request(url, comment):
    """
    API를 조회하는 함수

    Args:
        url (str): REST API URL
        comment (str): API REQUEST 종류 로깅

    Returns:
        jsons: response
    """
    print(f'REQUEST URL ({comment}): {url}')
    # 데이터를 가져올 Request 객체를 생성한다.
    req = request.Request(url)

    try:
        # 데이터를 조회한다.
        response = request.urlopen(req)

        # 200: 성공
        # 404: 페이지 찾을 수 없음
        # 502: 서버 네트워크 연결 실패

        # Http Code가 200일 경우 통신 성공
        if response.getcode() == 200:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(e)
        print(f'Error for URL : {url}')
        return None


def duplication_check_code(conn, sql):
    """
    테이블을 조회하여 영화코드 중복여부를 확인한다.

    Args:
        conn (MockConnection): DB Connection
        sql (str): SQL

    Returns:
        bool: 중복여부
    """

    result = conn.execute(sql).fetchone()
    if result is None:
        return True
    else:
        return bool(result[0])
