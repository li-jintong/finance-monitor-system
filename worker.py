# 必须放在最顶端！
import eventlet
eventlet.monkey_patch()

from celery import Celery
import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 注意：这里如果 DBAlertRule 定义在 main.py 里，需要导入它
from models import DBAlertRule
from notifier import send_wechat_alert
# 配置 Celery
celery_app = Celery('finance_tasks', broker='redis://localhost:6379/0')

# ... 剩下的代码保持不变 ...

# 2. 这里的任务逻辑和你之前的代码几乎一样，但它是异步执行的

@celery_app.task
def check_all_alerts_task():
    engine = create_engine("sqlite:///./finance.db")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        rules = db.query(DBAlertRule).all()
        if not rules:
            print("--- 账本为空，跳过检查 ---")
            return

        # 1. 性能优化：提取所有唯一的 symbol
        symbols = list(set([r.symbol for r in rules]))
        symbols_str = " ".join(symbols) # 变成 "BTC-USD AAPL"
        
        # 2. 批量抓取价格 (这一步极快！)
        tickers = yf.Tickers(symbols_str)
        # 获取所有最新价格，存入字典方便查询
        price_map = {s: tickers.tickers[s].fast_info['last_price'] for s in symbols}
        
        print(f"--- 批量巡检中，当前价格表: {price_map} ---")

        for rule in rules:
            current_price = price_map.get(rule.symbol)
            if current_price is None: continue
            
            # 3. 调试：不管有没有触发，先在控制台打印对比结果
            print(f"检查 {rule.symbol}: 现价 {current_price} vs 目标 {rule.target_price}")

            if current_price > rule.target_price:
                print(f"🔥 达到触发条件！正在发送微信...")
                title = f"🚨 价格预警: {rule.symbol}"
                content = f"现价 {current_price:.2f} 已超过目标价 {rule.target_price}"
                res = send_wechat_alert(title, content)
                print(f"微信接口返回结果: {res}")
    finally:
        db.close()

# 设定定时任务逻辑
celery_app.conf.beat_schedule = {
    'every-minute-check': {
        'task': 'worker.check_all_alerts_task', # 运行哪个任务
        'schedule': 60.0,                      # 每 60 秒运行一次
    },
}