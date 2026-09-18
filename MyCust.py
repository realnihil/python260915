from __future__ import annotations

import sqlite3
from pathlib import Path


class CustomerManager:
    def __init__(self, db_path: str = "MyCust.db") -> None:
        database_path = Path(db_path)
        if not database_path.is_absolute():
            database_path = Path(__file__).resolve().parent / database_path

        self.db_path = database_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Customers (
                custID INTEGER PRIMARY KEY AUTOINCREMENT,
                custName TEXT NOT NULL,
                custTitle TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def add_customer(self, cust_name: str, cust_title: str) -> int:
        cursor = self.connection.execute(
            "INSERT INTO Customers (custName, custTitle) VALUES (?, ?)",
            (cust_name, cust_title),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def get_customers(self, keyword: str = "") -> list[sqlite3.Row]:
        normalized_keyword = keyword.strip()
        if normalized_keyword:
            search_pattern = f"%{normalized_keyword}%"
            cursor = self.connection.execute(
                """
                SELECT custID, custName, custTitle
                FROM Customers
                WHERE custName LIKE ? OR custTitle LIKE ?
                ORDER BY custID ASC
                """,
                (search_pattern, search_pattern),
            )
        else:
            cursor = self.connection.execute(
                """
                SELECT custID, custName, custTitle
                FROM Customers
                ORDER BY custID ASC
                """
            )
        return cursor.fetchall()

    def update_customer(
        self,
        cust_id: int,
        cust_name: str,
        cust_title: str,
    ) -> bool:
        cursor = self.connection.execute(
            """
            UPDATE Customers
            SET custName = ?, custTitle = ?
            WHERE custID = ?
            """,
            (cust_name, cust_title, cust_id),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_customer(self, cust_id: int) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM Customers WHERE custID = ?",
            (cust_id,),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        self.connection.close()


''' main() 함수는 MyCust.py 파일이 직접 실행될 때만 호출됩니다.
    왜냐하면 밑에 if __name__ == "__main__": 조건문이 있기 때문입니다.
    그리고, return 문이 없고 (-> None) 이 씌여있어서
    반환을 하지 않습니다.'''
def main() -> None:
    from PySide6.QtWidgets import QApplication

    from MyCustGUI import CustomerView

    application = QApplication([])
    manager = CustomerManager()
    manager.create_table()
    window = CustomerView(manager)
    window.show()
    application.aboutToQuit.connect(manager.close)
    application.exec()

''' MyCust.py 에서 F5로 혹은 python MyCust.py 로 실행하면 
아래 main() 함수가 호출되어 GUI 프로그램이 실행됩니다. '''
if __name__ == "__main__":
    main()