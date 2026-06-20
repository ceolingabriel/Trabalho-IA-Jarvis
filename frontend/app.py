import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.core.agent import interagir_com_jarvis
from backend.core.learning import gerar_exercicio_active_recall, avaliar_resposta_aluno, gerar_guia_revisao

st.set_page_config(page_title="JARVIS IA", page_icon="🤖", layout="wide")
st.title("🤖 JARVIS")

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# WIDGET DE NOTÍCIAS — deve ficar ANTES do chat
# =========================================================
noticias_exemplo = [
    {"emoji": "🔐", "title": "Riscos de Cibersegurança e IA em 2026", "link": "https://itshow.com.br/risco-ciberseguranca-ia-software-infraestrutura-2026/"},
    {"emoji": "🤖", "title": "Problemas no RAG e 5 Formas de Corrigir", "link": "https://www.ibm.com/br-pt/think/insights/rag-problems-five-ways-to-fix"},
    {"emoji": "🚗", "title": "Tesla Muda de Rota: Foco no Robô Optimus", "link": "https://www.euronews.com/next/2026/01/29/tesla-changes-lanes"},
    {"emoji": "⚙️", "title": "A Corrida dos Robôs Humanoides", "link": "https://www.barrons.com/articles/tesla-optimus-robot-boston-dynamics-unitree-eb0a6abc"},
    {"emoji": "🛒", "title": "Robôs Optimus para o Público em 2027", "link": "https://www.bloomberg.com/news/articles/2026-01-22/tesla-venderia-robots-optimus"},
]

links_html = "\n".join([
    f'<div class="news-item"><span>{n["emoji"]}</span><a href="{n["link"]}" target="_blank">{n["title"]}</a></div>'
    for n in noticias_exemplo
])

st.markdown(f"""
<style>
.main .block-container {{ padding-right: 300px !important; }}
.news-widget {{
    position: fixed;
    top: 80px;
    right: 20px;
    width: 270px;
    background: linear-gradient(145deg, #1e1e1e, #121212);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 16px;
    z-index: 99999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    font-family: 'Segoe UI', sans-serif;
}}
.news-header {{
    font-size: 11px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    text-align: center;
}}
.news-item {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #2a2a2a;
}}
.news-item:last-child {{ border-bottom: none; }}
.news-item span {{ font-size: 18px; flex-shrink: 0; margin-top: 2px; }}
.news-item a {{
    font-size: 13px;
    color: #ddd;
    text-decoration: none;
    line-height: 1.4;
}}
.news-item a:hover {{ color: #00A2FF; }}
</style>

<div class="news-widget">
    <div class="news-header">📰 Notícias em Destaque</div>
    {links_html}
</div>
""", unsafe_allow_html=True)

# =========================================================
# CHAT PRINCIPAL
# =========================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Fale com o JARVIS")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("JARVIS está pensando e consultando o sistema..."):
        historico_formatado = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
        
        # INÍCIO DA MODIFICAÇÃO: Tratamento de Erro do Streamlit
        try:
            resposta_jarvis = interagir_com_jarvis(prompt, historico=historico_formatado)
            
            st.chat_message("assistant").markdown(resposta_jarvis)
            st.session_state.messages.append({"role": "assistant", "content": resposta_jarvis})
            
        except Exception as e:
            # Exibe um bloco vermelho amigável e fixo em vez da tela inteira de erro
            st.error("⚠️ Ocorreu um erro de comunicação com os servidores da IA. Verifique sua chave de API ou sua conexão.")
            print(f"[Log de Erro] Falha na chamada da API: {e}")
        # FIM DA MODIFICAÇÃO

# =========================================================
# BARRA LATERAL: MELHORIAS DE APRENDIZADO 
# =========================================================
with st.sidebar:
    st.header("🧠 Modo Aprendizado")
    st.caption("Baseado nos seus PDFs (RAG)")
    
    topico = st.text_input("Qual tópico deseja revisar agora?")
    
    if st.button("Gerar Exercício"):
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
    st.divider()
    st.subheader("📋 Guia de Revisão")
    
    if st.button("Gerar Guia de Revisão"):
        with st.spinner("Gerando guia..."):
            guia = gerar_guia_revisao(topico)
            st.session_state.guia_atual = guia

    if "guia_atual" in st.session_state:
        st.markdown(st.session_state.guia_atual)