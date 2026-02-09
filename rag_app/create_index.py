import requests
import json

BASE_URL = "http://localhost:8080"
INDEX_NAME = "documents"

payload = {
    "name": INDEX_NAME,
    "dimension": 384,
    "metric": "cosine"
}

response = requests.post(
    f"{BASE_URL}/api/v1/index/create",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

print("Status Code:", response.status_code)
print("Response:", response.text)


