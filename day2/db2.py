# db1.py
import sqlite3

#연결객체(파일에 영구적 저장)
conn = sqlite3.connect(r'c:\work\day2\sample.db')
#커서객체 생성
cur = conn.cursor()
#테이블 생성
cur.execute('Create Table PhoneBook (name text, phone text);')
#1건 입력
cur.execute('Insert Into PhoneBook (name, phone) values ("홍길동", "010-1234-5678");')

#입력 매개변수 처리
name = "김철수"
phoneNum = "010-9876-5432"
cur.execute('Insert Into PhoneBook (name, phone) values (?, ?);', (name, phoneNum))

#여러건 입력
datalist = [("박영희", "010-1111-2222"), ("이순신", "010-3333-4444")]
cur.executemany('Insert Into PhoneBook (name, phone) values (?, ?);', datalist)

#검색
cur.execute('Select * From PhoneBook;')

for row in cur:
    print(row[0], row[1])

#정상적 완료
conn.commit()

# print('----fetchone()----')
# print(cur.fetchone())
# print('----fetchmany(2)----')
# print(cur.fetchmany(2))
# print('----fetchall()----')
# print(cur.fetchall())