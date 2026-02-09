import requests
import numpy as np

BASE_URL = "http://localhost:8080"
INDEX_NAME = "documents"

# dummy vector (384-dim)
vector = np.random.rand(384).tolist()

payload = {
    "index": INDEX_NAME,
    "id": "test_1",
    "vector": vector,
    "metadata": {
        "text": "This is a test document chunk"
    }
}

response = requests.post(
    f"{BASE_URL}/api/v1/vector/insert",
    json=payload
)

print("Status:", response.status_code)
print("Response:", response.text)
