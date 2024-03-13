import websocket
import threading
import time
import requests
import json

API_KEY = 'oSh7LrJcfP6JYZBXcmpaa3m7a34bQyCVgErOUIg2qDJhCiq5OCw6eiRJ9TunOpqo'
API_SECRET = 'rJ5Bsn3MIgLjEZ54wXaqHU4DAx38I9ACl0wLqOj9TzqFSApTmRJqtR9kgb97tJXH'
BASE_URL = 'https://api.binance.com'
WS_BASE_URL = 'wss://stream.binance.com:9443/ws'
symbol = 'btcusdt'  # Используйте свою переменную symbol

def on_message(ws, message):
    print("Received message: ", message)

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code=None, close_msg=None):
    print("Connection closed", close_status_code, close_msg)
    # Переподключение
    time.sleep(10)
    connect_to_websocket()

def on_open(ws):
    print("Connection opened")
    # Подписываемся на потоки
    subscribe_message = json.dumps({
        "method": "SUBSCRIBE",
        "params": [
            f"{symbol}@aggTrade",
            f"{symbol}@kline_1m"
        ],
        "id": 1
    })
    ws.send(subscribe_message)

def create_listen_key():
    response = requests.post(f"{BASE_URL}/api/v3/userDataStream", headers={"X-MBX-APIKEY": API_KEY})
    data = response.json()
    return data['listenKey']

def renew_listen_key(listen_key):
    requests.put(f"{BASE_URL}/api/v3/userDataStream?listenKey={listen_key}", headers={"X-MBX-APIKEY": API_KEY})

def connect_to_websocket():
    listen_key = create_listen_key()
    ws_url = f"{WS_BASE_URL}/{listen_key}"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

def renew_key_periodically():
    while True:
        time.sleep(2700)  # 45 минут
        listen_key = create_listen_key()
        renew_listen_key(listen_key)

if __name__ == "__main__":
    # Запускаем WebSocket соединение в отдельном потоке
    ws_thread = threading.Thread(target=connect_to_websocket)
    ws_thread.start()

    # Обновляем listen_key каждые 45 минут
    renew_thread = threading.Thread(target=renew_key_periodically)
    renew_thread.start()
