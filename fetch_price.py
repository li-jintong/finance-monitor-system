import yfinance as yf

def get_real_price(symbol: str):
    # 模拟会计查询实时汇率/股价
    ticker = yf.Ticker(symbol)
    # 拿到最新的市场价
    data = ticker.fast_info
    return data['last_price']

# 测试一下
if __name__ == "__main__":
    price = get_real_price("BTC-USD") # 获取比特币价格
    print(f"当前 BTC 价格是: {price}")