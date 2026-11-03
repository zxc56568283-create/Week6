import requests

# Hacker News 的 robots.txt 網址
url = "https://news.ycombinator.com/robots.txt"

# 設定 headers 模擬正常瀏覽器請求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("--- Hacker News robots.txt 內容 ---")
    print(response.text)
    print("-----------------------------------")
    
    # 簡單解析內容
    lines = response.text.strip().split("\n")
    disallow_list = []
    crawl_delay = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("Disallow:"):
            disallow_list.append(line.split(":", 1)[1].strip())
        elif line.startswith("Crawl-delay:"):
            crawl_delay = line.split(":", 1)[1].strip()
            
    print(f"(1) Crawl-delay: {crawl_delay} 秒")
    print(f"(2) User-agent: * 禁止項目: {', '.join(disallow_list)}")
else:
    print(f"連線失敗，狀態碼: {response.status_code}")