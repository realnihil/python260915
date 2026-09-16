from pathlib import Path

import openpyxl


output_path = Path(__file__).resolve().parent.parent / "ProductList.xlsx"

workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.title = "제품목록"

worksheet.append(["제품ID", "제품명", "가격", "수량"])

product_types = [
    "노트북",
    "스마트폰",
    "태블릿",
    "모니터",
    "키보드",
    "마우스",
    "헤드셋",
    "스피커",
    "카메라",
    "프린터",
]

for product_id in range(1, 101):
    product_type = product_types[(product_id - 1) % len(product_types)]
    price = 30000 + product_id * 12500
    quantity = (product_id * 7) % 50 + 1
    worksheet.append([product_id, f"{product_type} {product_id:03d}", price, quantity])

worksheet.column_dimensions["A"].width = 12
worksheet.column_dimensions["B"].width = 20
worksheet.column_dimensions["C"].width = 14
worksheet.column_dimensions["D"].width = 10

workbook.save(output_path)
print(f"전자제품 {worksheet.max_row - 1}개를 {output_path}에 저장했습니다.")