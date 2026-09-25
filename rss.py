import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os

url = "https://www.kri.or.jp/news-event/"
response = requests.get(url)
response.encoding = response.apparent_encoding
lines = response.text.splitlines()
cleaned = "\n".join([l for l in lines if l.strip() != ""])
# fg
fg = FeedGenerator()
fg.title("けいはんな_ニュース・イベント")
fg.link(href=url)
fg.description("kri_rss")

path = './response.txt'

# 取得したhtmlをパース
soup = BeautifulSoup(response.text, "html.parser")
items = soup.select("div.news-item")

for item in items:
    # div.news-title>a要素を取得
    title_tag = item.select_one("div.news-title a")
    # noneの際のエラーハンドリング
    if title_tag is None:
        continue
    # stripは直前の空白を詰める
    title = title_tag.get_text(strip=True)
    link = title_tag["href"]
    date_tag = item.select_one("span.date")
    if date_tag is None:
        continue
    date = date_tag.get_text(strip=True)
    print(date, title, link)
# generate xml
    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)

print(response.status_code)
os.path.join("feed.xml")
fg.rss_file("feed.xml")

# response write to file
os.path.join(path)

with open(path, mode='w') as f:
    f.write(cleaned)

