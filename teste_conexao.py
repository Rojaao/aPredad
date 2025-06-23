
import websocket
import json

# COLE SEU TOKEN AQUI:
TOKEN = "QeLHyXPtiQJtJYb"

def on_open(ws):
    print("✅ Conexão aberta! Enviando token para autenticação...")
    auth_msg = {
        "authorize": TOKEN
    }
    ws.send(json.dumps(auth_msg))

def on_message(ws, message):
    data = json.loads(message)
    print("📩 Mensagem recebida:")
    print(json.dumps(data, indent=2))

    if data.get("msg_type") == "authorize":
        print("✅ Token autorizado com sucesso!")
        ticks_msg = {
            "ticks_history": "R_100",
            "adjust_start_time": 1,
            "count": 10,
            "end": "latest",
            "start": 1,
            "style": "ticks"
        }
        ws.send(json.dumps(ticks_msg))

    if data.get("msg_type") == "history":
        print("✅ Histórico de ticks recebido com sucesso!")
        ws.close()

def on_error(ws, error):
    print(f"❌ Erro: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexão fechada.")

websocket.enableTrace(False)
ws = websocket.WebSocketApp(
    "wss://ws.deriv.com/websockets/v3?app_id=1089",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
