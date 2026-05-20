import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.core.agent import interagir_com_jarvis
from backend.core.learning import gerar_exercicio_active_recall, avaliar_resposta_aluno


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

# =========================================================
# BARRA LATERAL: MELHORIAS DE APRENDIZADO 
# =========================================================
with st.sidebar:
    st.header("🧠 Modo Aprendizado")
    st.caption("Baseado nos seus PDFs (RAG)")
    
    topico = st.text_input("Qual tópico deseja revisar agora?")
    
    if st.button("Gerar Exercício (Active Recall)"):
        with st.spinner("Lendo materiais..."):
            st.session_state.pergunta_atual = gerar_exercicio_active_recall(topico)
            st.session_state.topico_atual = topico
            
    
    if "pergunta_atual" in st.session_state:
        st.info(st.session_state.pergunta_atual)
        resposta_aluno = st.text_area("Sua resposta:")
        
        if st.button("Avaliar Minha Resposta"):
            with st.spinner("Avaliando..."):
                avaliacao = avaliar_resposta_aluno(
                    st.session_state.pergunta_atual, 
                    resposta_aluno, 
                    st.session_state.topico_atual
                )
                st.success(avaliacao)