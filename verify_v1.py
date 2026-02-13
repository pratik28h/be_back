import requests
import os
import time

BASE_URL = "http://127.0.0.1:8003"
API_V1 = f"{BASE_URL}/api/v1/data_sources"

# Dummy token
HEADERS = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaWRkaGVzaDI5MDlAZ21haWwuY29tIiwiZXhwIjoxNzcxMzEzMDUzfQ.bzRRtcspXEH-h00PN9x9je53pjDAMtD3i00Am-UZSrg"}

def create_test_file():
    content = "id,name,age,city\n1,John,25,New York\n2,Jane,,London\n3,Bob,30,Pairs"
    with open("test_v1.csv", "w") as f:
        f.write(content)

def test_upload_v1():
    print("Testing v1/upload...")
    files = {'file': ('test_v1.csv', open('test_v1.csv', 'rb'), 'text/csv')}
    response = requests.post(f"{API_V1}/upload", files=files, headers=HEADERS)
    if response.status_code == 200:
        print("Upload Success:", response.json())
    else:
        print("Upload Failed:", response.text)

def test_list_files():
    print("\nTesting v1/all...")
    response = requests.get(f"{API_V1}/all", headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print("List Success. Files:", [f['filename'] for f in data['files']])
    else:
        print("List Failed:", response.text)

def test_get_file():
    print("\nTesting v1/get-file...")
    response = requests.get(f"{API_V1}/get-file/test_v1.csv", headers=HEADERS)
    if response.status_code == 200:
        print("Get File Success. Rows:", len(response.json()['data']))
    else:
        print("Get File Failed:", response.text)

def test_preview_cleaning():
    print("\nTesting v1/preview (remove nulls)...")
    payload = {
        "filename": "test_v1.csv",
        "command": "remove nulls"
    }
    response = requests.post(f"{API_V1}/preview", json=payload, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print("Preview Success. Diff:", data['diff_summary'])
    else:
        print("Preview Failed:", response.text)

def test_preprocess():
    print("\nTesting v1/preprocess (remove nulls)...")
    payload = {
        "filename": "test_v1.csv",
        "command": "remove nulls"
    }
    response = requests.post(f"{API_V1}/preprocess", json=payload, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print("Preprocess Success:", data['message'])
    else:
        print("Preprocess Failed:", response.text)

if __name__ == "__main__":
    create_test_file()
    time.sleep(1)
    
    try:
        test_upload_v1()
        test_list_files()
        test_get_file()
        test_preview_cleaning()
        test_preprocess()
    except Exception as e:
        print("Verification failed:", e)
