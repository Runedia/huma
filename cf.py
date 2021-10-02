"""
공통적으로 사용하는 변수를 관리한다.

최초 작성일: 2021-09-30
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-09-30 | 1.0.0 | 김지호 | 최초작성
"""

# 영화진흥위원회(http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do) OpenAPI Key
# API_KEY = '5ae88f21ef91305b8eb978447797ee72' # 2021-10-01 만료
# API_KEY = '39ea868a51e1d043da825b0cde0981b2' # 2021-10-01 만료
# API_KEY = 'eec39ee4692d829911723511a238286d'
API_KEY = 'f5eef3421c602c6cb7ea224104795888'
# API_KEY = 'e214869aee06cd8dcb7b1a2f103fdbc7'

# DB INFO - MySQL
DB_HOST = 'runedia.kro.kr'
DB_PORT = '6033'
DB_USERNAME = 'huma'
DB_PASSWORD = 'xf1ub1faxqtz8xq5'
DB_NAME = 'huma'
DB_URL = f'mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# TABLE NAME
MOVIE_LIST = 'movielist'
MOVIE_INFO = 'movieinfo'
COMPANY_LIST = 'companylist'
PEOPLE_LIST = 'peoplelist'
BOXOFFICE_LIST = 'boxofficelist'

# 공통코드

# repNationCd (http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml?key={API_KEY}&comCode=2204)
KOREA = '22041011'
USA = '22042002'
JAPAN = '22041008'

# movieTypeCd (http://kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml?key={API_KEY}&comCode=2201)
FEATURE = '220101'

