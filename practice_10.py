import requests

# 蝦皮購物 robots.txt 網址
url = "https://shopee.tw/robots.txt"

# 模擬真實瀏覽器標頭，避免遭蝦皮防爬機制阻擋 (403 Forbidden)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    content = response.text
    print("=== 成功讀取 shopee.tw robots.txt ===\n")
    
    # 逐行解析各 User-agent 對應的 Crawl-delay
    current_agent = None
    crawl_delays = {}
    
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("user-agent:"):
            current_agent = line.split(":", 1)[1].strip()
        elif line.lower().startswith("crawl-delay:") and current_agent:
            delay = line.split(":", 1)[1].strip()
            crawl_delays[current_agent] = delay

    print(f"(1) 一般爬蟲 (User-agent: *) 的 Crawl-delay: {crawl_delays.get('*', '未特別標示')} 秒")
    print(f"(2) Googlebot 的 Crawl-delay: {crawl_delays.get('Googlebot', '未特別標示')} 秒")
else:
    print(f"讀取失敗，HTTP 狀態碼: {response.status_code}")