import requests

url = "http://localhost:8000/v1/chat/completions"
payload = {
    "messages": [{"role": "user", "content": "Can you explain how machine learning works?"}]
}

response = requests.post(url, json=payload)
print(response.json())