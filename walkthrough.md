# SentinelStream: Real-time Fraud Detection System

SentinelStream is a real-time fraud detection platform that processes financial transactions and flags suspicious activities using a rule-based engine. It features a modern dashboard for monitoring transactions and alerts.

## 🚀 Key Features

*   **Real-time Analysis**: Processes transactions instantly as they occur.
*   **Rule Engine**: Configurable fraud detection rules (High Amount, Velocity, Location mismatch).
*   **Interactive Dashboard**: Live monitoring of transaction feed and alert status.
*   **REST API**: Full API documentation available via Swagger UI.
*   **Containerized**: Fully dockerized for easy deployment.

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI
*   **Frontend**: HTML5, CSS3, JavaScript (Nginx)
*   **Database**: PostgreSQL
*   **Infrastructure**: Docker, Docker Compose

## 🏁 Quick Start

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd sentinelstream
    ```

2.  **Start the application**:
    ```bash
    docker-compose up -d --build
    ```

3.  **Access the interfaces**:
    *   **Dashboard**: [http://localhost:3000](http://localhost:3000)
    *   **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing

Run the test suite to verify the backend logic:

```bash
# Run tests inside the container
docker-compose exec backend pytest
```

## 📸 Overview

The system monitors transaction streams and assigns a risk score based on predefined rules. High-risk transactions are flagged or blocked in real-time, providing immediate protection against fraudulent activities.
