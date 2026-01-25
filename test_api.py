import requests
import json

url = "http://localhost:8000/api/v1/transactions/"
headers = {"Content-Type": "application/json"}
data = {
    "user_id": "test1",
    "amount": 100,
    "currency": "USD",
    "transaction_type": "deposit"
}

print("Testing API...")
response = requests.post(url, headers=headers, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
