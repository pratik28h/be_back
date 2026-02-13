import requests
import os
import time

BASE_URL = "http://127.0.0.1:8000"

def test_upload():
    print("Testing /upload...")
    files = {'file': ('test.csv', open('test.csv', 'rb'), 'text/csv')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    if response.status_code == 200:
        print("Upload Success:", response.json().keys())
    else:
        print("Upload Failed:", response.text)

def test_chat_remove_nulls():
    print("\nTesting /chat (remove nulls)...")
    payload = {"message": "please remove null rows"}
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("Chat Success:", data.keys())
        print("Message:", data['message'])
        print("Rows:", data['rows'])
    else:
        print("Chat Failed:", response.text)

def test_chat_insights():
    print("\nTesting /chat (insights check)...")
    payload = {"message": "drop column city"}
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        print("Drop Column Success")
        print("Charts created:", response.json().get('charts'))
    else:
        print("Chat Failed:", response.text)

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(2) 
    try:
        test_upload()
        test_chat_remove_nulls()
        test_chat_insights()
    except Exception as e:
        print("Verification failed:", e)
