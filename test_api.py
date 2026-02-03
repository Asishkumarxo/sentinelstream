import requests
import json

# URL adjusted (removed trailing slash based on router definition if needed, 
# but router defines @router.post("/") so path is /api/v1/transactions/)
url = "http://localhost:8000/api/v1/transactions/"
headers = {"Content-Type": "application/json"}
data = {
    "user_id": "test1",
    "amount": 100,
    "currency": "USD",
    "merchant": "Amazon",
    "transaction_type": "deposit"
}

print("Testing API...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
