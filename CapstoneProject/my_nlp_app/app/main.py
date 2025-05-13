from app import create_app
from flask import Flask
import requests
import nltk
import matplotlib.pyplot as plt

app = create_app()

@app.route('/')
def check_connection():
    try:
        response = requests.get("https://www.google.com", timeout=3)
        return f"Status Code: {response.status_code}, Connected to Google!"
    except requests.exceptions.RequestException as e:
        return f"Connection failed: {e}"

if __name__ == '__main__':
    with app.test_client() as client:

        print('\n📦 테스트 요청 시작...\n')
        response = client.post('/test', json={'text': 'Flask is good!'})
        print('✅ 응답 결과:', response.get_json(), '\n')

    app.run(host='0.0.0.0', port=5000)