# DemoForm2.py
# DemoForm2.ui(화면단) + DemoForm2.py(로직단)
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

# 크롤링을 위한 선언
from bs4 import BeautifulSoup
import urllib.request
#정규표현식
import re

# UI파일 로딩
form_class = uic.loadUiType("DemoForm2.ui")[0]

# DemoForm 클래스 정의(QMainWindow 상속)
class DemoForm(QMainWindow, form_class):
    # 초기화 메서드
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def firstClick(self):
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

        self.label.setText("중고장터 크롤링 완료!")
    def secondClick(self):
            self.label.setText("두번째 버튼을 클릭")
    def thirdClick(self):
            self.label.setText("세번째 버튼을 클릭")

# 진입점을 체크(직접 이 모듈을 실행)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    sys.exit(app.exec())