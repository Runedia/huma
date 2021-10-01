"""
데이터베이스와 연결하는 메인 로직
Database Management Tool

최초 작성일: 2021-09-30
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-09-30 | 1.0.0 | 김지호 | 최초작성
"""

import pymysql
from sqlalchemy import create_engine
from cf import DB_URL

# 데이터베이스 접속을 위해 사전 실행하는 코드
pymysql.install_as_MySQLdb()


class SingletonInstane:
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__get_instance
        return cls.__instance


class DBM(SingletonInstane):
    def __init__(self):
        # DB 연결 설정
        print(f'DB_URL: {DB_URL}')
        self.engine = create_engine(DB_URL, encoding='utf8', echo=False)

        # DB 연결
        self.conn = self.engine.connect()


engine = DBM.instance().engine
conn = DBM.instance().conn
