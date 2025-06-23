
import streamlit as st
import websocket
import json
import threading

st.set_page_config(page_title="Teste de Conexão Deriv", layout="centered")
st.title("🔌 Teste de Conexão com a Deriv")

token = st.text_input("🔑 Cole seu token da Deriv (demo ou real)", type="password")

status_box = st.empty()
log_box = st.empty()

def testar_conexao(token):
    logs = []

    def log(msg):
        logs.append(msg)
        log_box.code("\n".join(logs), language="text")

    def on_open(ws):
        log("✅ Conexão aberta! Enviando token...")
        auth_msg = {
            "authorize": token
        }
        ws.send(json.dumps(auth_msg))

    def on_message(ws, message):
        data = json.loads(message)
        log("📩 Mensagem recebida:")
        log(json.dumps(data, indent=2))

        if data.get("msg_type") == "authorize":
            log("✅ Token autorizado com sucesso!")
            ticks_msg = {
                "ticks_history": "R_100",
                "adjust_start_time": 1,
                "count": 10,
                "end": "latest",
                "start": 1,
                "style": "ticks"
            }
            ws.send(json.dumps(ticks_msg))

        elif data.get("msg_type") == "history":
            log("✅ Histórico de ticks recebido com sucesso!")
            ws.close()

    def on_error(ws, error):
        log(f"❌ Erro: {error}")

    def on_close(ws, close_status_code, close_msg):
        log("🔌 Conexão encerrada.")

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        "wss://ws.deriv.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()

if st.button("▶ Testar Conexão com Deriv"):
    if not token:
        st.warning("⚠️ Insira um token válido.")
    else:
        status_box.info("⏳ Testando conexão...")
        threading.Thread(target=testar_conexao, args=(token,)).start()
