# 🚀 Real-Time Finance Monitor & Alert System

A high-performance backend system built with Python, designed for **24/7 automated surveillance** of financial assets (Stocks, Cryptocurrencies, etc.) with real-time push notifications.



## 🌟 Key Features

* **Asynchronous Decoupled Architecture**: Leveraged the **Producer-Consumer model** using **FastAPI, Celery, and Redis** to isolate I/O-intensive tasks (API scraping) from the core business logic.
* **Performance Optimization**: Engineered a **Batch Processing** strategy that reduced multi-asset polling latency from **8.6s to 0.8s**, achieving a **10x performance boost**.
* **Modular Design**: Implemented a clean separation of the `models` layer to resolve **Circular Import** issues, enhancing system maintainability and scalability.
* **Automated Alerting**: Integrated **Webhook** protocols (ServerChan/Feishu/Lark) to ensure sub-second delivery of price volatility alerts.

## 🛠️ Tech Stack

* **Web Framework**: FastAPI
* **Task Scheduling**: Celery & Celery Beat
* **Message Broker**: Redis
* **Persistence Layer**: SQLAlchemy (SQLite)
* **Data Source**: Yahoo Finance API (yfinance)


