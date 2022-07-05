# SQL Module

# 1. Create Class : Database()
# 2. 클래스 생성 시 pymysql.connect() 함수를 사용해 DB 정보 입력할건데 기본 뼈대인 __init()__ 함수 만들고 여기다가 pymysql.connect() 를 만들자
# 3. execute() 함수 -> 매개변수 sql, values ==> SQL 구문을 수행하는데 values 집어넣어서 수행
# 4. execute_all() 함수 -> 매개변수 sql, values ==> SQL 구문 수행 ===> values 넣고 결과값을 받아와서 데이터프레임으로 전환 후 리턴
# 5. commit() 함수 -> DB에 commit하는 함수
# 단 execute(), execute_all() 함수에서 매개변수 values 기본값을 [] 빈 리스트로 지정


import pymysql
import pandas as pd

class Database():
    # 뼈대를 만들어 봅시다
    def __init__(self):
        # 당연하겠지만 뭐 하나 틀리면 나락갑니다
        self._db = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '1234',
            db = 'ubion4',
            port = 3306 # mysql default port
        )

        self.cursor = self._db.cursor(pymysql.cursors.DictCursor)

    # SQL 구문을 실행 -> INSERT, DELETE 등등
    def execute(self, sql, values=[]):
        self.cursor.execute(sql, values)

    # SQL 구문을 실행 -> SELECT ONLY, 그리고 그 결과를 데이터프레임으로 리턴
    def execute_all(self, sql, values=[]):
        self.cursor.execute(sql, values)
        self.result = self.cursor.fetchall()
        return self.result
        #return pd.DataFrame(self.result)

    # INSERT, DELETE 등등 DB에 저장된 데이터 작업 후 실제 DB에 반영시켜주는 commit()
    def commit(self):
        self._db.commit()

    # 워크밴치 등과의 통신 오류로 SQL 자체에 문제가 있는 경우 통신을 종료하기 위해 일부러 넣어둔 거지 실제로 쓰진 않을겁니다 아마도
    def close(self):
        self._db.close()


# CLASS vs. function
# pd.DataFrame() -> Pandas 라이브러리의 클래스를 사용함
# pd.merge() -> Pandas 라이브러리의 함수를 사용함
# 둘이 어떻게 구분하냐 -> 클래스는 이름의 첫 글자를 대문자로 표시하는 관습 아닌 관습이 있다
# 클래스가 아니고서야 self 가 들어갈 이유는 없어요. 함수에서는 매개변수만 잘 표시해주면 될 뿐이야