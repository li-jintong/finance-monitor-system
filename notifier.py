import httpx

# 填入你刚才复制的 SendKey
SEND_KEY = "SCT308980TTPLISNujNKVQ9eAoVizO4QFR"

def send_wechat_alert(title: str, content: str):
    url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"
    data = {
        "title": title,
        "desp": content  # desp 是正文内容
    }
    with httpx.Client() as client:
        response = client.post(url, data=data)
        return response.json()