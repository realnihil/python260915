# web2.py

# <span class="subject_fixed" data-role="list-title-text" title="아이폰17프로 256 실버">
# 							아이폰17프로 256 실버
# 						</span>

# 크롤링을 위한 선언
from bs4 import BeautifulSoup
import urllib.request

#정규표현식
import re

f = open('clien.txt', 'wt', encoding='utf-8')

hdr = {'User-Agent': 'Mozilla/5.0'}

# 페이징처리
for i in range(0, 10):
    url = f'https://www.clien.net/service/board/sold?&od=T31&category=0&po={i}'
    print(url)

    # 요청객체
    req = urllib.request.Request(url, headers=hdr)
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, 'html.parser')

    for tag in soup.find_all('span', attrs={'data-role': 'list-title-text'}):
        title = tag.text.strip()
        title = title.replace('\n', '')
        if re.search('아이폰', title):
            print(title)
            f.write(title + '\n')

f.close()