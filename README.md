# 🚀 实时金融资产监控预警系统 (Finance Monitor System)

这是一个基于 Python 的工业级后端系统，旨在实现 7x24 小时的全自动金融资产（股票、加密货币等）价格巡检与实时报警。

## 🌟 项目亮点
- **异步解耦架构**：采用 **FastAPI + Celery + Redis** 生产消费者模型，将 I/O 密集型任务（API 抓取）与业务逻辑分离。
- **极致性能优化**：通过 **Batch Processing（批处理）** 技术，将多资产轮询延迟从 **8.6s 降低至 0.8s**，性能提升逾 10 倍。
- **模块化解耦**：合理拆分 `models` 层，解决复杂项目中的 `Circular Import` 依赖问题。
- **自动化预警**：集成 **Webhook** 协议（Server酱/飞书），实现价格波动的秒级触达。

## 🛠️ 技术栈
- **Web 框架**: FastAPI
- **任务调度**: Celery & Celery Beat
- **消息代理**: Redis
- **持久化层**: SQLAlchemy (SQLite)
- **数据来源**: Yahoo Finance API

## 📋 快速开始

### 1. 环境准备
```bash
git clone [https://github.com/YourUsername/finance-monitor.git](https://github.com/YourUsername/finance-monitor.git)
cd finance-monitor
pip install -r requirements.txt
```
### 2. 启动 Redis
```
确保你的 Redis 服务已运行在 localhost:6379。
```
### 3. 运行系统
```
需开启三个独立终端窗口：

API 服务: uvicorn main:app --reload

后台 Worker: celery -A worker worker --loglevel=info -P eventlet

定时调度: celery -A worker beat --loglevel=info
```
## 性能对比
```
方案,100个资产巡检耗时,系统响应能力
初版 (同步/单次),~8.6s,极低（容易阻塞）
优化版 (异步/批量),~0.8s,极高（异步非阻塞）
```
## 预警效果展示
```
<img width="1125" height="2436" alt="image" src="https://github.com/user-attachments/assets/689df053-9b1a-405a-b0ad-eaf26361f113" />
```
