# Trabalho-IA-Jarvis

Assistente acadêmico com chat, RAG sobre PDFs, gerenciamento de tarefas, agenda, módulo de aprendizado (Active Recall) e logs de observabilidade via Tool Calling (ReAct).

## Stack

- Frontend: Streamlit
- Backend: Python 3.10
- IA: Cliente OpenAI-compatible (google/gemma-3-12b-it)
- Banco: SQLite (Nativo)
- RAG: FAISS + sentence-transformers (all-MiniLM-L6-v2)
- Runtime: Ambiente Virtual Isolado (Conda)

## Executar Localmente

Ative o ambiente do projeto:

```bash
conda activate jarvis_env
