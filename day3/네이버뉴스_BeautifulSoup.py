import requests
import openpyxl
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SEARCH_URL = (
    "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&"
    "fbm=0&acr=1&acq=%EB%B0%98%EB%8F%84%EC%B2%B4&qdt=0&ie=utf8&"
    "query=%EB%B0%98%EB%8F%84%EC%B2%B4&ackey=oerk11xq"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def make_news_search_url(url):
    """일반 네이버 검색 URL을 뉴스 검색 URL로 바꾼다."""
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["where"] = "news"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))


def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def crawl_news_results(url, limit=10):
    """네이버 뉴스 검색 결과에서 제목, 요약, 기사 링크를 가져온다."""
    soup = get_soup(make_news_search_url(url))
    results = []
    seen_links = set()

    for title_span in soup.select("span.sds-comps-text-type-headline1"):
        title_link = title_span.find_parent("a", href=True)
        if title_link is None or not title_link["href"].startswith("http"):
            continue

        link = title_link["href"]
        if link in seen_links:
            continue

        item = title_span.find_parent(
            "div", class_=lambda value: value and "sds-comps-vertical-layout" in value
        )
        summary = ""
        if item:
            summary_tag = item.select_one("span.sds-comps-text-type-body1")
            if summary_tag:
                summary = summary_tag.get_text(" ", strip=True)

        results.append(
            {
                "title": title_span.get_text(" ", strip=True),
                "summary": summary,
                "link": link,
            }
        )
        seen_links.add(link)

        if len(results) >= limit:
            break

    return results


def crawl_article_content(url):
    """네이버 기사 페이지에서 본문 텍스트를 가져온다."""
    soup = get_soup(url)
    content = soup.select_one("#dic_area, #newsct_article, #articeBody")
    if content is None:
        return ""

    for tag in content.select("script, style"):
        tag.decompose()
    return content.get_text(" ", strip=True)


def save_results_to_excel(news_list, filename="naver_result.xlsx"):
    """크롤링한 뉴스 결과를 엑셀 파일로 저장한다."""
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "네이버 뉴스"

    worksheet.append(["번호", "제목", "요약", "기사 링크"])

    for index, news in enumerate(news_list, start=1):
        worksheet.append(
            [index, news["title"], news["summary"], news["link"]]
        )

    worksheet.column_dimensions["A"].width = 8
    worksheet.column_dimensions["B"].width = 45
    worksheet.column_dimensions["C"].width = 100
    worksheet.column_dimensions["D"].width = 80
    worksheet.freeze_panes = "A2"

    workbook.save(filename)


if __name__ == "__main__":
    news_list = crawl_news_results(SEARCH_URL, limit=10)

    for index, news in enumerate(news_list, start=1):
        print(f"[{index}] {news['title']}")
        print(f"요약: {news['summary']}")
        print(f"링크: {news['link']}")
        print("-" * 80)

    print(f"총 {len(news_list)}건 수집")
    save_results_to_excel(news_list)
    print("naver_result.xlsx 파일 저장 완료")
