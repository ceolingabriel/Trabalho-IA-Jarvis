import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.core.agent import interagir_com_jarvis


st.set_page_config(page_title="JARVIS Acadêmico", page_icon="🤖", layout="wide")
st.title("🤖 JARVIS - Assistente Pessoal Acadêmico")


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# CHAT PRINCIPAL 
# =========================================================
prompt = st.chat_input("Fale com o JARVIS")

if prompt:
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    with st.spinner("JARVIS está pensando e consultando o sistema..."):
        
        historico_formatado = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
        
        
        resposta_jarvis = interagir_com_jarvis(prompt, historico=historico_formatado)

   
    st.chat_message("assistant").markdown(resposta_jarvis)
    st.session_state.messages.append({"role": "assistant", "content": resposta_jarvis})
