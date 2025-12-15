import requests
import json
import time

url = "http://localhost:5000/api/symptom-search"
payload = {"query": "I have a headache and fever"}
headers = {"Content-Type": "application/json"}

print(f"Sending request to {url}...")
try:
    start = time.time()
    response = requests.post(url, json=payload, headers=headers)
    duration = time.time() - start
    print(f"Request took {duration:.2f}s")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:", json.dumps(response.json(), indent=2))
    except:
        print("Raw Response:", response.text)
except Exception as e:
    print(f"Error: {e}")
