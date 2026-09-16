import sqlite3
from pathlib import Path


class ProductList:
    def __init__(self, db_path="MyProduct.db"):
        self.db_path = Path(__file__).parent / db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def insert_product(self, product_id, product_name, product_price):
        self.conn.execute(
            """
            INSERT INTO Products (productID, productName, productPrice)
            VALUES (?, ?, ?)
            """,
            (product_id, product_name, product_price),
        )
        self.conn.commit()

    def update_product(self, product_id, product_name=None, product_price=None):
        updates = []
        values = []

        if product_name is not None:
            updates.append("productName = ?")
            values.append(product_name)
        if product_price is not None:
            updates.append("productPrice = ?")
            values.append(product_price)

        if not updates:
            return

        values.append(product_id)
        self.conn.execute(
            f"UPDATE Products SET {', '.join(updates)} WHERE productID = ?",
            values,
        )
        self.conn.commit()

    def delete_product(self, product_id):
        self.conn.execute(
            "DELETE FROM Products WHERE productID = ?",
            (product_id,),
        )
        self.conn.commit()

    def select_products(self, product_id=None):
        if product_id is None:
            cursor = self.conn.execute(
                "SELECT productID, productName, productPrice "
                "FROM Products ORDER BY productID"
            )
        else:
            cursor = self.conn.execute(
                "SELECT productID, productName, productPrice "
                "FROM Products WHERE productID = ?",
                (product_id,),
            )
        return cursor.fetchall()

    def prepare_sample_data(self, count=1000):
        products = [
            (product_id, f"전자제품 {product_id}", 10000 + product_id * 100)
            for product_id in range(1, count + 1)
        ]
        self.conn.executemany(
            """
            INSERT OR REPLACE INTO Products
                (productID, productName, productPrice)
            VALUES (?, ?, ?)
            """,
            products,
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == "__main__":
    with ProductList() as product_list:
        product_list.prepare_sample_data(1000)
        products = product_list.select_products()
        print(f"Products 테이블에 {len(products)}개의 샘플 데이터를 준비했습니다.")
        print("첫 번째 제품:", products[0])