import websocket
import json
import threading
import time

WS_URL = 'wss://stream.bybit.com/v5/public/linear'

def on_message(ws, message):
    print("Received message: ", message)

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code=None, close_msg=None):
    print("Connection closed", close_status_code, close_msg)
    time.sleep(10)
    connect_to_websocket()

def on_open(ws):
    print("Connection opened")
    # Подписываемся на поток сделок
    ws.send(json.dumps({
        "op": "subscribe",
        "args": [
            "publicTrade.BTCUSDT"
        ]
    }))
    # Подписываемся на поток свечей
    ws.send(json.dumps({
        "op": "subscribe",
        "args": [
            "kline.5.BTCUSDT"
        ]
    }))

def connect_to_websocket():
    ws = websocket.WebSocketApp(WS_URL,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

# Запускаем WebSocket соединение в отдельном потоке
if __name__ == "__main__":
    thread = threading.Thread(target=connect_to_websocket)
    thread.start()
