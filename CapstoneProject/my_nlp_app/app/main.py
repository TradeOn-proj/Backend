from app import create_app, socket_io
from app.socket_handlers import register_socketio_handlers
from flask import Flask
from flask_socketio import SocketIO
import requests
import nltk
import matplotlib.pyplot as plt

app = create_app()
socket_io = SocketIO(app, async_mode='threading')

register_socketio_handlers(socket_io)

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

        response = client.get('/api/v1/users/{user1}/trades')
        print('✅ 응답 결과:', response.get_json(), '\n')

        response = client.post('/api/v1/users/register',json={"username" : "user1"})
        print('✅ 응답 결과:', response.get_json(), '\n')

    socket_io.run(app, host='0.0.0.0', port=5000, debug= True, use_reloader= False)