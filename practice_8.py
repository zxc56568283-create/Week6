import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 設定 logging 模組
# 將日誌同時寫入檔案 week_06_ex3_Quotes_login.log 與終端機螢幕
log_filename = "week_06_ex3_Quotes_login.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("開始執行爬蟲程式：課堂練習 - 3")

# 2. 建立 Session 並執行登入
session = requests.Session()
login_url = "http://quotes.toscrape.com/login"

try:
    # 取得登入頁面與 csrf_token
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    # 提交登入表單（可輸入任意帳密）
    payload = {
        "csrf_token": csrf_token,
        "username": "student",
        "password": "password"
    }
    login_response = session.post(login_url, data=payload)
    logging.info("成功登入 Quotes to Scrape 網站")

except Exception as e:
    logging.error(f"登入失敗或取得 CSRF Token 錯誤: {e}")
    raise SystemExit(e)

# 3. 逐頁爬取名言資料
quotes_data = []
page = 1
base_url = "http://quotes.toscrape.com"
current_url = f"{base_url}/page/{page}/"

while True:
    logging.info(f"正在爬取第 {page} 頁: {current_url}")
    page_res = session.get(current_url)
    page_soup = BeautifulSoup(page_res.text, "html.parser")
    
    quote_elements = page_soup.find_all("div", class_="quote")
    
    # 記錄每一頁抓到的名言數量
    count = len(quote_elements)
    logging.info(f"第 {page} 頁爬取完成，共抓取到 {count} 句名言")
    
    # 解析名言內容
    for item in quote_elements:
        quote_text = item.find("span", class_="text").get_text(strip=True)
        author = item.find("small", class_="author").get_text(strip=True)
        tag_elements = item.find_all("a", class_="tag")
        tags = ";".join([t.get_text(strip=True) for t in tag_elements])
        
        quotes_data.append({
            "page": page,
            "quote": quote_text,
            "author": author,
            "tags": tags
        })
    
    # 判斷是否有下一頁（檢視是否存在 class 為 next 的 li 標籤）
    next_li = page_soup.find("li", class_="next")
    if next_li and next_li.find("a"):
        next_path = next_li.find("a")["href"]
        current_url = base_url + next_path
        page += 1
    else:
        logging.info("已到達最後一頁，結束爬取。")
        break

# 4. 存檔為 quotes_all.csv
df = pd.DataFrame(quotes_data)
df = df[["page", "quote", "author", "tags"]]
output_csv = "quotes_all.csv"
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

logging.info(f"全部爬取完畢！總計 {len(df)} 筆資料，已儲存至 {output_csv}")
logging.info(f"日誌已成功儲存至 {log_filename}")