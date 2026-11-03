import requests

url = "https://www.moneydj.com/robots.txt"

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
    lines = content.splitlines()

    current_agent = None
    agent_rules = {}

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("user-agent:"):
            current_agent = line.split(":", 1)[1].strip()
            if current_agent not in agent_rules:
                agent_rules[current_agent] = {"allow": [], "disallow": []}
        elif current_agent:
            if line.lower().startswith("allow:"):
                rule = line.split(":", 1)[1].strip()
                agent_rules[current_agent]["allow"].append(rule)
            elif line.lower().startswith("disallow:"):
                rule = line.split(":", 1)[1].strip()
                agent_rules[current_agent]["disallow"].append(rule)

    # 1. 取得一般爬蟲 (*) 的 Allow 項目
    general_allows = agent_rules.get("*", {}).get("allow", [])
    print(f"(1) 一般爬蟲 (User-agent: *) 明確標示允許項目：共 {len(general_allows)} 項")
    for item in general_allows:
        print(f"    - Allow: {item}")

    # 2. 列出針對 AI / 特定訓練封鎖的爬蟲
    known_ai_bots = {
        "gptbot", "chatgpt-user", "ccbot", "google-extended", 
        "claudebot", "anthropic-ai", "bytespider", "perplexitybot", "facebookbot"
    }

    blocked_ai_bots = []
    for agent, rules in agent_rules.items():
        if "/" in rules["disallow"] and agent.lower() in known_ai_bots:
            blocked_ai_bots.append(agent)

    print("\n(2) 被全面封鎖 (Disallow: /) 的 AI 訓練相關爬蟲：")
    for bot in blocked_ai_bots:
        print(f"    - {bot}")

else:
    print(f"連線失敗，狀態碼: {response.status_code}")