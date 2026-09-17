import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ProductDatabase:
    def __init__(self, database_name="MyProduct2.db"):
        self.database_path = database_name
        self.connection = sqlite3.connect(self.database_path)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS MyProduct (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
            """
        )
        self.connection.commit()

    def create_id(self):
        today_prefix = int(date.today().strftime("%Y%m%d"))
        first_id = today_prefix * 10000
        last_id = first_id + 9999
        row = self.connection.execute(
            "SELECT COALESCE(MAX(id), ?) FROM MyProduct WHERE id BETWEEN ? AND ?",
            (first_id, first_id, last_id),
        ).fetchone()
        next_id = row[0] + 1
        if next_id > last_id:
            raise ValueError("오늘 생성할 수 있는 제품 번호가 모두 사용되었습니다.")
        return next_id

    def insert(self, name, price):
        product_id = self.create_id()
        self.connection.execute(
            "INSERT INTO MyProduct (id, name, price) VALUES (?, ?, ?)",
            (product_id, name, price),
        )
        self.connection.commit()

    def update(self, product_id, name, price):
        self.connection.execute(
            "UPDATE MyProduct SET name = ?, price = ? WHERE id = ?",
            (name, price, product_id),
        )
        self.connection.commit()

    def delete(self, product_id):
        self.connection.execute("DELETE FROM MyProduct WHERE id = ?", (product_id,))
        self.connection.commit()

    def find(self, product_id=None, name=""):
        if product_id is not None:
            return self.connection.execute(
                "SELECT id, name, price FROM MyProduct WHERE id = ? ORDER BY id",
                (product_id,),
            ).fetchall()
        if name:
            return self.connection.execute(
                "SELECT id, name, price FROM MyProduct WHERE name LIKE ? ORDER BY id",
                (f"%{name}%",),
            ).fetchall()
        return self.connection.execute(
            "SELECT id, name, price FROM MyProduct ORDER BY id"
        ).fetchall()

    def close(self):
        self.connection.close()


class BicycleProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = ProductDatabase()
        self.setWindowTitle("자전거용품 관리")
        self.resize(820, 620)
        self.setMinimumSize(700, 520)
        self.build_ui()
        self.load_products()

    def build_ui(self):
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("자동 생성 또는 검색할 번호")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("자전거용품 이름")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("가격(원)")

        form_layout = QFormLayout()
        form_layout.addRow("제품 ID", self.id_input)
        form_layout.addRow("제품명", self.name_input)
        form_layout.addRow("가격", self.price_input)

        input_button = QPushButton("입력")
        update_button = QPushButton("수정")
        delete_button = QPushButton("삭제")
        search_button = QPushButton("검색")
        clear_button = QPushButton("전체보기")
        input_button.setObjectName("primaryButton")
        update_button.setObjectName("secondaryButton")
        delete_button.setObjectName("dangerButton")
        search_button.setObjectName("searchButton")
        clear_button.setObjectName("ghostButton")
        input_button.clicked.connect(self.insert_product)
        update_button.clicked.connect(self.update_product)
        delete_button.clicked.connect(self.delete_product)
        search_button.clicked.connect(self.search_products)
        clear_button.clicked.connect(self.show_all_products)

        button_layout = QHBoxLayout()
        for button in (input_button, update_button, delete_button, search_button, clear_button):
            button_layout.addWidget(button)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["제품 ID", "제품명", "가격(원)"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.cellDoubleClicked.connect(self.select_product)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(34, 28, 34, 30)
        layout.setSpacing(14)

        title = QLabel("BIKE GEAR  /  INVENTORY")
        title.setObjectName("titleLabel")
        subtitle = QLabel("자전거용품을 빠르게 등록하고 한눈에 관리하세요")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        table_title = QLabel("등록된 자전거용품")
        table_title.setObjectName("sectionLabel")
        layout.addWidget(table_title)
        layout.addWidget(self.table)
        self.setCentralWidget(central_widget)
        self.setStyleSheet(
            """
            QMainWindow {
                background: #dceff0;
            }
            QWidget#centralWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f2fbf7, stop: 0.55 #dff2f1, stop: 1 #cfe6f0
                );
            }
            QLabel {
                color: #183746;
                font-size: 13px;
                font-weight: 600;
            }
            QLabel#titleLabel {
                min-height: 42px;
                color: #087f78;
                font-size: 28px;
                font-weight: 900;
                letter-spacing: 2px;
            }
            QLabel#subtitleLabel {
                min-height: 26px;
                color: #52717a;
                font-size: 14px;
                font-weight: 400;
                margin-top: 0;
                margin-bottom: 6px;
            }
            QLabel#sectionLabel {
                color: #163c4b;
                font-size: 17px;
                font-weight: 800;
                margin-top: 8px;
            }
            QLineEdit {
                min-height: 38px;
                padding: 0 13px;
                border: 1px solid #8fb9c0;
                border-radius: 9px;
                background: rgba(255, 255, 255, 210);
                color: #173746;
                selection-background-color: #1bbca4;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0db7a5;
                background: #ffffff;
            }
            QLineEdit::placeholder {
                color: #75949d;
            }
            QPushButton {
                min-height: 42px;
                padding: 0 18px;
                border: 0;
                border-radius: 9px;
                color: #07131c;
                font-size: 14px;
                font-weight: 800;
            }
            QPushButton:hover {
                border: 2px solid #ffffff;
            }
            QPushButton:pressed {
                padding-top: 2px;
            }
            QPushButton#primaryButton {
                background: #41d7bd;
            }
            QPushButton#primaryButton:hover {
                background: #8bffe5;
            }
            QPushButton#secondaryButton {
                background: #72b9ff;
            }
            QPushButton#secondaryButton:hover {
                background: #a6d4ff;
            }
            QPushButton#dangerButton {
                background: #ff7890;
            }
            QPushButton#dangerButton:hover {
                background: #ff9cac;
            }
            QPushButton#searchButton {
                background: #ffc857;
            }
            QPushButton#searchButton:hover {
                background: #ffdc83;
            }
            QPushButton#ghostButton {
                color: #214753;
                border: 1px solid #75a5ae;
                background: rgba(255, 255, 255, 170);
            }
            QPushButton#ghostButton:hover {
                background: #ffffff;
            }
            QTableWidget {
                gridline-color: #c2dce0;
                border: 1px solid #8fb9c0;
                border-radius: 11px;
                background: rgba(255, 255, 255, 225);
                alternate-background-color: #eaf7f6;
                color: #234351;
                font-size: 14px;
                selection-background-color: #55cfc0;
                selection-color: #ffffff;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #d1e5e7;
            }
            QHeaderView::section {
                min-height: 38px;
                border: 0;
                border-bottom: 2px solid #0db7a5;
                background: #b9e8e2;
                color: #145d60;
                font-size: 13px;
                font-weight: 900;
            }
            QScrollBar:vertical {
                width: 10px;
                background: #c9e2e5;
            }
            QScrollBar::handle:vertical {
                min-height: 30px;
                border-radius: 5px;
                background: #62b9b5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            QMessageBox {
                background: #e5f4f3;
            }
            QMessageBox QLabel {
                color: #183746;
            }
            """
        )

    @staticmethod
    def display_id(product_id):
        value = str(product_id)
        return f"{value[:4]}-{value[4:6]}-{value[6:8]}-{value[8:]}"

    @staticmethod
    def parse_id(value):
        digits = re.sub(r"[^0-9]", "", value.strip())
        if not digits:
            return None
        if len(digits) != 12:
            raise ValueError("제품 ID는 YYYY-MM-DD-0000 형식이어야 합니다.")
        return int(digits)

    def read_product_fields(self, require_id=False):
        product_id = self.parse_id(self.id_input.text())
        if require_id and product_id is None:
            raise ValueError("수정하거나 삭제할 제품을 선택하세요.")
        name = self.name_input.text().strip()
        if not name:
            raise ValueError("제품명을 입력하세요.")
        price_text = self.price_input.text().replace(",", "").strip()
        if not price_text.isdigit():
            raise ValueError("가격은 0 이상의 정수로 입력하세요.")
        return product_id, name, int(price_text)

    def insert_product(self):
        try:
            _, name, price = self.read_product_fields()
            self.database.insert(name, price)
            self.clear_inputs()
            self.load_products()
        except (ValueError, sqlite3.IntegrityError) as error:
            self.show_error(str(error))

    def update_product(self):
        try:
            product_id, name, price = self.read_product_fields(require_id=True)
            self.database.update(product_id, name, price)
            self.load_products()
        except ValueError as error:
            self.show_error(str(error))

    def delete_product(self):
        try:
            product_id = self.parse_id(self.id_input.text())
            if product_id is None:
                raise ValueError("삭제할 제품을 선택하세요.")
            self.database.delete(product_id)
            self.clear_inputs()
            self.load_products()
        except ValueError as error:
            self.show_error(str(error))

    def search_products(self):
        try:
            product_id = self.parse_id(self.id_input.text())
            products = self.database.find(product_id, self.name_input.text().strip())
            self.display_products(products)
        except ValueError as error:
            self.show_error(str(error))

    def show_all_products(self):
        self.clear_inputs()
        self.load_products()

    def load_products(self):
        self.display_products(self.database.find())

    def display_products(self, products):
        self.table.setRowCount(len(products))
        for row, (product_id, name, price) in enumerate(products):
            id_item = QTableWidgetItem(self.display_id(product_id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item = QTableWidgetItem(f"{price:,}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, price_item)

    def select_product(self, row, _column):
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text())

    def clear_inputs(self):
        self.id_input.clear()
        self.name_input.clear()
        self.price_input.clear()

    @staticmethod
    def show_error(message):
        QMessageBox.warning(None, "입력 확인", message)

    def closeEvent(self, event):
        self.database.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BicycleProductWindow()
    window.show()
    sys.exit(app.exec())