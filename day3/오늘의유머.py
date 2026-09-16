# <td class="subject">
# <a href="/board/view.php?table=humordata&amp;no=2059996&amp;s_no=15626812&amp;kind=total&amp;page=1" target="_top"> 요리사가 받을수 있는 최고의 극찬</a>  <span style="margin-left:4px;"><img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;"> </span><img src="//www.todayhumor.co.kr/board/images/list_icon_shovel.gif?2" alt="펌글" style="margin-right:3px;top:2px;position:relative"> </td>


# 크롤링을 위한 선언
from bs4 import BeautifulSoup
import urllib.request

#정규표현식
import re

f = open('todayhumor.txt', 'wt', encoding='utf-8')

hdr = {'User-Agent': 'Mozilla/5.0'}

# 페이징처리
for i in range(1, 11):
    url = f'https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page={i}'
    print(url)

    # 요청객체
    req = urllib.request.Request(url, headers=hdr)
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, 'html.parser')

    for tag in soup.find_all('td', attrs={'class': 'subject'}):
        title = tag.a.text.strip()
        title = title.replace('\n', '')
        if re.search('한국', title):
            print(title)
            f.write(title + '\n')

f.close()