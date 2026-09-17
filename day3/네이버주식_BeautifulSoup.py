import csv
import html
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


MARKET_URL = "https://stock.naver.com/market/stock/kr"
MARKET_API_URL = "https://stock.naver.com/api/domestic/market/stock/default"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def get_soup(url, params=None):
    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "html.parser")


def crawl_market_page(url=MARKET_URL):
    """네이버 국내 주식 화면이 사용하는 API 결과를 BeautifulSoup으로 읽는다."""
    return crawl_stock_list("KOSPI")


def crawl_stock_list(market_type="KOSPI"):
    """API 응답을 HTML 표로 만든 후 BeautifulSoup으로 종목을 추출한다."""
    response = requests.get(
        MARKET_API_URL,
        params={"marketType": market_type},
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    items = response.json()

    rows = []
    for item in items:
        name = html.escape(str(item.get("itemname", "")))
        code = html.escape(str(item.get("itemcode", "")))
        rows.append(
            "<tr>"
            f'<td class="name"><a href="/domestic/stock/{code}/price">{name}</a></td>'
            f'<td>{html.escape(str(item.get("nowPrice", "")))}</td>'
            f'<td>{html.escape(str(item.get("prevChangeRate", "")))}%</td>'
            f'<td>{html.escape(str(item.get("tradeVolume", "")))}</td>'
            f'<td>{html.escape(str(item.get("marketSum", "")))}</td>'
            "</tr>"
        )

    table_html = (
        '<table><thead><tr><th>종목</th><th>현재가</th><th>등락률</th>'
        "<th>거래량</th><th>시가총액(원)</th></tr></thead>"
        f'<tbody>{"".join(rows)}</tbody></table>'
    )
    soup = BeautifulSoup(table_html, "html.parser")
    stocks = []

    for row in soup.select("table tbody tr"):
        cells = row.select("td")
        if len(cells) != 5:
            continue

        values = [cell.get_text(" ", strip=True) for cell in cells]
        name_tag = cells[0].select_one("a[href]")
        stocks.append(
            {
                "종목": values[0],
                "현재가": values[1],
                "등락률": values[2],
                "거래량": values[3],
                "시가총액(원)": values[4],
                "링크": urljoin(MARKET_URL, name_tag["href"]),
            }
        )

    return stocks


def save_csv(stocks, filename="naver_stocks.csv"):
    output_path = Path(__file__).resolve().parent / filename
    fieldnames = list(stocks[0].keys()) if stocks else [
        "종목",
        "현재가",
        "전일비",
        "등락률",
        "시가총액(억)",
        "거래량",
        "링크",
    ]

    with output_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stocks)

    return output_path


if __name__ == "__main__":
    stocks = crawl_stock_list("KOSPI") + crawl_stock_list("KOSDAQ")

    for stock in stocks[:20]:
        print(
            f"{stock['종목']} | 현재가: {stock['현재가']} | "
            f"등락률: {stock['등락률']} | 거래량: {stock['거래량']}"
        )

    output_path = save_csv(stocks)
    print(f"총 {len(stocks)}개 종목 수집")
    print(f"CSV 저장 위치: {output_path}")