
import streamlit as st
from bot_core import iniciar_robo
import time

st.set_page_config(page_title="Predador de Padrões - por Rogger", layout="centered")
st.title("🧠 Predador de Padrões")
st.markdown("**por Rogger**")

# Inicialização de variáveis globais
if "status" not in st.session_state:
    st.session_state.status = "⏸️ Parado"
if "historico" not in st.session_state:
    st.session_state.historico = []
if "lucro_total" not in st.session_state:
    st.session_state.lucro_total = 0.0
if "parar" not in st.session_state:
    st.session_state.parar = False

token = st.text_input("🔑 Insira seu token da Deriv (demo ou real)", type="password")
stake = st.number_input("💰 Stake inicial (R$)", min_value=0.35, value=1.00, step=0.01)
martingale = st.number_input("🎯 Fator de Martingale", min_value=1.0, value=2.0, step=0.1)
stop_loss = st.number_input("⛔ Stop Loss (R$)", min_value=1.0, value=60.0)
take_profit = st.number_input("✅ Meta de Lucro (R$)", min_value=1.0, value=50.0)
delay = st.slider("⏱️ Delay entre entradas (segundos)", 1, 30, 7)
analise_ticks = st.selectbox("📊 Analisar quantos últimos dígitos?", [10, 20, 50])

# Botões
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Iniciar Robô"):
        if token:
            st.session_state.status = "🚀 Rodando..."
            st.session_state.parar = False
            st.success("Robô iniciado!")
            iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks)
        else:
            st.warning("⚠️ Por favor, insira um token válido.")

with col2:
    if st.button("⛔ Parar Robô"):
        st.session_state.parar = True
        st.session_state.status = "⏸️ Parado"
        st.info("Robô foi pausado manualmente.")

# Status e lucro
st.subheader("📈 Status do Robô")
st.info(f"Status atual: {st.session_state.status}")
st.metric(label="💰 Lucro Acumulado (USD)", value=f"${st.session_state.lucro_total:.2f}")

# Histórico das operações
if st.session_state.historico:
    st.subheader("🧾 Histórico das Entradas")
    st.table(st.session_state.historico[::-1])

# Áudio para WIN e LOSS
with st.sidebar:
    st.subheader("🔊 Sons de Resultado")
    st.audio("win.mp3")
    st.audio("loss.mp3")
