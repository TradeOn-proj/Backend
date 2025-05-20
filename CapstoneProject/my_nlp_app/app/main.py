from . import create_app
from flask import Flask
import requests
import nltk
import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy ORM import
from dotenv import load_dotenv  # .env 파일 로드용 모듈
import os  # 환경변수 사용을 위한 모듈
from sqlalchemy import text  # SQL 테스트용 쿼리 실행

load_dotenv(dotenv_path=".env")
app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # RDS 연결 문자열
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/ping')
def ping():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ RDS 연결 성공", 200
    except Exception as e:
        return f"❌ RDS 연결 실패: {str(e)}", 500

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