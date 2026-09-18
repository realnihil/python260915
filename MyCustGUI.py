from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CustomerView(QMainWindow):
    def __init__(self, manager: Any) -> None:
        super().__init__()
        self.manager = manager
        self.setWindowTitle("고객정보 관리")
        self.resize(760, 520)
        self.setup_ui()
        self.connect_signals()
        self.load_customers()

    def setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        title_label = QLabel("고객정보 관리")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        action_group = QGroupBox("작업")
        action_layout = QGridLayout(action_group)
        self.add_button = QPushButton("입력")
        self.update_button = QPushButton("수정")
        self.delete_button = QPushButton("삭제")
        self.search_button = QPushButton("검색")
        action_layout.addWidget(self.add_button, 0, 0)
        action_layout.addWidget(self.update_button, 0, 1)
        action_layout.addWidget(self.delete_button, 1, 0)
        action_layout.addWidget(self.search_button, 1, 1)

        form_group = QGroupBox("고객정보")
        form_layout = QGridLayout(form_group)
        self.id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.title_edit = QLineEdit()
        self.search_edit = QLineEdit()
        self.id_edit.setReadOnly(True)
        self.search_edit.setPlaceholderText("이름 또는 직위 검색")
        form_layout.addWidget(QLabel("고객 ID"), 0, 0)
        form_layout.addWidget(self.id_edit, 0, 1)
        form_layout.addWidget(QLabel("고객 이름"), 1, 0)
        form_layout.addWidget(self.name_edit, 1, 1)
        form_layout.addWidget(QLabel("고객 직위"), 2, 0)
        form_layout.addWidget(self.title_edit, 2, 1)
        form_layout.addWidget(QLabel("검색어"), 3, 0)
        form_layout.addWidget(self.search_edit, 3, 1)

        top_layout = QHBoxLayout()
        top_layout.addWidget(action_group)
        top_layout.addWidget(form_group, 1)

        self.customer_table = QTableWidget(0, 3)
        self.customer_table.setHorizontalHeaderLabels(
            ["고객 ID", "고객 이름", "고객 직위"]
        )
        self.customer_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.customer_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.customer_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.customer_table.horizontalHeader().setStretchLastSection(True)
        self.customer_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.customer_table, 1)

    def connect_signals(self) -> None:
        self.add_button.clicked.connect(self.on_add_clicked)
        self.update_button.clicked.connect(self.on_update_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.customer_table.cellClicked.connect(self.on_table_row_selected)
        self.search_edit.returnPressed.connect(self.on_search_clicked)

    def load_customers(self, keyword: str = "") -> None:
        customers = self.manager.get_customers(keyword)
        self.customer_table.setRowCount(0)

        for row_index, customer in enumerate(customers):
            self.customer_table.insertRow(row_index)
            values = (customer["custID"], customer["custName"], customer["custTitle"])
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.customer_table.setItem(row_index, column_index, item)

        self.customer_table.resizeColumnsToContents()

    def clear_inputs(self) -> None:
        self.id_edit.clear()
        self.name_edit.clear()
        self.title_edit.clear()

    def _get_customer_values(self) -> tuple[str, str] | None:
        cust_name = self.name_edit.text().strip()
        cust_title = self.title_edit.text().strip()
        if not cust_name or not cust_title:
            QMessageBox.warning(self, "입력 확인", "고객 이름과 직위를 입력하세요.")
            return None
        return cust_name, cust_title

    def _get_selected_id(self) -> int | None:
        try:
            return int(self.id_edit.text())
        except ValueError:
            QMessageBox.warning(self, "선택 확인", "먼저 고객 목록에서 고객을 선택하세요.")
            return None

    def on_add_clicked(self) -> None:
        values = self._get_customer_values()
        if values is None:
            return

        cust_id = self.manager.add_customer(*values)
        self.load_customers()
        self.id_edit.setText(str(cust_id))
        self._select_table_row(cust_id)
        QMessageBox.information(self, "입력 완료", "고객정보를 입력했습니다.")

    def on_update_clicked(self) -> None:
        cust_id = self._get_selected_id()
        values = self._get_customer_values()
        if cust_id is None or values is None:
            return

        if self.manager.update_customer(cust_id, *values):
            self.load_customers()
            self._select_table_row(cust_id)
            QMessageBox.information(self, "수정 완료", "고객정보를 수정했습니다.")
        else:
            QMessageBox.warning(self, "수정 실패", "고객정보를 찾을 수 없습니다.")

    def on_delete_clicked(self) -> None:
        cust_id = self._get_selected_id()
        if cust_id is None:
            return

        answer = QMessageBox.question(
            self,
            "삭제 확인",
            "선택한 고객정보를 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        if self.manager.delete_customer(cust_id):
            self.load_customers(self.search_edit.text())
            self.clear_inputs()
            QMessageBox.information(self, "삭제 완료", "고객정보를 삭제했습니다.")
        else:
            QMessageBox.warning(self, "삭제 실패", "고객정보를 찾을 수 없습니다.")

    def on_search_clicked(self) -> None:
        self.load_customers(self.search_edit.text())

    def on_table_row_selected(self, row: int, column: int) -> None:
        del column
        values = [
            self.customer_table.item(row, column_index).text()
            for column_index in range(self.customer_table.columnCount())
        ]
        self.id_edit.setText(values[0])
        self.name_edit.setText(values[1])
        self.title_edit.setText(values[2])

    def _select_table_row(self, cust_id: int) -> None:
        for row_index in range(self.customer_table.rowCount()):
            item = self.customer_table.item(row_index, 0)
            if item and item.text() == str(cust_id):
                self.customer_table.selectRow(row_index)
                return
