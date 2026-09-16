# web1.py
from bs4 import BeautifulSoup

#웹페이지를 로딩
page = open(r'C:\work\day3\Chap09_test.html', 'rt', encoding='UTF8').read()
# 검색이 용이한 스프 객체
soup = BeautifulSoup(page, 'html.parser')   
#전체 페이지를 출력
# print(soup.prettify())
# 첫번째 <p> 태그만 검색
# print(soup.find('p'))

#조건검색: <p class='outer-text'> 만 검색
# print(soup.find_all('p', class_ = 'outer-text'))

#print(soup.find_all('p', attrs = {'class':'outer-text'}))

#print(soup.find('p', id='first'))

#태그 내부에 문자열만 가져오기: text 속성
for tag in soup.find_all('p'):
    title = tag.text.strip()
    title =title.replace('\n', '')
    print(title)

f = open('demo.txt', 'wt', encoding='utf-8')
f.write('첫번째\n두번째\n세번째\n')
f.close()  

f = open('demo.txt', 'rt', encoding='utf-8')
result = f.read()
print(result)
f.close

#문자열 처리
data = '<<< 안녕하세요. 반갑습니다.>>>'
result = data.strip('<> ')
print(result)

result2 = result.replace('안녕하세요', 'Hello')
print(result2)

#리스트로 변경
lst = result2.split()
print(lst)

result3 = '  '.join(lst)
print(result3)


#정규표현식
import re

result = re.search('[0-9]*th', '35th')
print(result)
print(result.group())

result = re.search('\d{4}', '올해는 2026년입니다.')
print(result)
print(result.group())

result = re.search('apple', 'this is apple')
print(result)
print(result.group())
