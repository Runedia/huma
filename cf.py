"""
공통적으로 사용하는 변수를 관리한다.

최초 작성일: 2021-09-30
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-09-30 | 1.0.0 | 김지호 | 최초작성
"""

# 영화진흥위원회(http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do) OpenAPI Key
API_KEY = '5ae88f21ef91305b8eb978447797ee72'

# DB INFO - MySQL
DB_HOST = 'runedia.kro.kr'
DB_PORT = '6033'
DB_USERNAME = 'huma'
DB_PASSWORD = 'huma2021^'
DB_NAME = 'huma'
DB_URL = f'mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# TABLE NAME
MOVIE_LIST = 'movielist'

# 공통코드

# repNationCd (http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml?key={API_KEY}&comCode=2204)
KOREA = '22041011'
USA = '22042002'
JAPAN = '22041008'

# movieTypeCd (http://kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml?key={API_KEY}&comCode=2201)
FEATURE = '220101'
