# 🛡️ SentinelStream - Real-time Fraud Detection System

SentinelStream is a full-stack, real-time transaction monitoring platform designed to detect and flag fraudulent financial activities. It processes incoming transaction streams, applies a configurable set of fraud detection rules, and visualizes the results on a live dashboard.

## 🚀 Key Features

*   **Real-time Processing**: Instantly analyzes transactions as they occur.
*   **Fraud Detection Engine**: Applies sophisticated rules including:
    *   **High Amount Checks**: Flags transactions exceeding a defined threshold.
    *   **Velocity Checks**: Detects rapid-fire transactions from the same user.
    *   **Location Analysis**: Identifies suspicious location changes.
    *   **New Merchant Flags**: Monitors interaction with previously unknown merchants.
*   **Interactive Dashboard**: A responsive web interface for analysts to monitor traffic and review flagged alerts in real-time.
*   **Robust API**: Fully documented RESTful API built with FastAPI.
*   **Data Integrity**: Persistent storage with PostgreSQL and schema management via Alembic.

## 🛠️ Technology Stack

*   **Backend**: Python 3.13, FastAPI, SQLAlchemy, Pydantic
*   **Database**: PostgreSQL
*   **Frontend**: HTML5, CSS3, Vanilla JavaScript (served via Nginx)
*   **Infrastructure**: Docker, Docker Compose

## 🏗️ Architecture Overview

The system follows a microservices-ready architecture:
1.  **Transaction API**: Receives transaction data via HTTP POST.
2.  **Fraud Engine**: Evaluates the transaction against active rules and assigns a risk score.
3.  **Database**: Stores transaction history and alert logs.
4.  **Frontend**: Polls the API for the latest feed and updates the UI dynamically.

## 🏁 Quick Start

Get the entire system running in minutes using Docker.

### Prerequisites
*   Docker & Docker Compose installed

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Asishkumarxo/sentinelstream.git
    cd sentinelstream
    ```

2.  **Start the application**:
    ```bash
    docker-compose up -d --build
    ```

3.  **Access the application**:
    *   **Dashboard**: [http://localhost:3000](http://localhost:3000)
    *   **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing

To run the backend test suite:

```bash
docker-compose exec backend pytest
```

## 📜 Project Status

✅ **Completed**: The project has successfully implemented all core modules:
*   Backend API & Logic
*   Database Integration & Migrations
*   Fraud Detection Algorithm
*   Frontend Dashboard & Deployment
