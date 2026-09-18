# Chap10_DemoButton.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QCoreApplication
import Chap10_ProductList

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        btn1 = QPushButton("열기", self)
        btn1.move(20, 20)
        form1 = Chap10_ProductList.DemoForm()
        btn1.clicked.connect(lambda: form1.show())
        # btn1.clicked.connect(QCoreApplication.instance().quit)

# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm()
    demoForm.show()
    app.exec()