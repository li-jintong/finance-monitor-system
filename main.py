from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import yfinance as yf
from models import Base, DBAlertRule

# --- 数据库配置 ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建数据库表
Base.metadata.create_all(bind=engine)

# --- 数据传输模型 (Pydantic Model) ---
class AlertCreate(BaseModel):
    user_id: int
    symbol: str
    target_price: float

app = FastAPI()

# 获取数据库连接的工具
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-alert")
def create_alert(rule: AlertCreate, db: Session = Depends(get_db)):
    # 将用户输入转为数据库记录
    new_rule = DBAlertRule(
        user_id=rule.user_id, 
        symbol=rule.symbol, 
        target_price=rule.target_price
    )
    db.add(new_rule) # 准备写入
    db.commit()      # 正式提交（会计里的过账）
    db.refresh(new_rule)
    return {"status": "success", "id": new_rule.id}

@app.get("/show-alerts")
def get_all_alerts(db: Session = Depends(get_db)):
    return db.query(DBAlertRule).all()



import yfinance as yf
from fastapi import HTTPException

# 接口 1: 单纯查询某个币种/股票的当前价格
@app.get("/check-market/{symbol}")
def check_market(symbol: str):
    # 逻辑校验：Symbol 通常是字符串，yfinance 自己会处理不存在的情况
    try:
        ticker = yf.Ticker(symbol)
        # 这里的 last_price 就是实时价格
        price = ticker.fast_info['last_price']
        
        if price is None:
            raise ValueError("价格获取不到")
            
        return {"symbol": symbol, "current_price": price}
    except Exception as e:
        # 报错处理：如果找不到这个代码，返回 404
        raise HTTPException(status_code=404, detail=f"无法获取 {symbol} 的价格，请检查输入")

"""
# 接口 2: 核心业务逻辑——检查某个用户的所有告警是否触发
@app.get("/check-alerts/{user_id}")
def check_user_alerts(user_id: int, db: Session = Depends(get_db)):
    # 1. 从数据库找出这个用户的所有规则 (相当于会计从账本调取客户合同)
    rules = db.query(DBAlertRule).filter(DBAlertRule.user_id == user_id).all()
    
    trigger_results = []
    
    for rule in rules:
        # 2. 获取该资产的实时价格
        ticker = yf.Ticker(rule.symbol)
        current_price = ticker.fast_info['last_price']
        
        # 3. 比对逻辑 (按你说的：大于才算触发)
        is_triggered = False
        if current_price > rule.target_price:
            is_triggered = True
            print(f"【报警】用户 {user_id} 的 {rule.symbol} 达到阈值！当前:{current_price}, 目标:{rule.target_price}")
        
        trigger_results.append({
            "symbol": rule.symbol,
            "target": rule.target_price,
            "current": current_price,
            "triggered": is_triggered
        })
        
    return {"user_id": user_id, "results": trigger_results}
"""

# 1. 导入后台任务


# 2. 创建一个“手动触发后台巡检”的接口
@app.post("/trigger-check")
def trigger_check():
    # 注意这里：不是直接调用函数，而是用 .delay()
    # 这一步相当于出纳员把凭证丢进会计的待办收件箱（Redis）
    from worker import check_all_alerts_task
    check_all_alerts_task.delay() 
    return {"message": "后台巡检任务已启动，请观察 Celery 窗口"}