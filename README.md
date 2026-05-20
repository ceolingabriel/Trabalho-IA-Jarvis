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
```

Suba o frontend e o backend simultaneamente:

```bash
streamlit run frontend/app.py
```
Acesse:

```Plaintext
Frontend: http://localhost:8501
```
O terminal exibirá os logs de execução do Streamlit. Para parar a aplicação, pressione Ctrl + C no terminal.

## Configuração da LLM
As chaves e os endpoints estão configurados diretamente no cliente OpenAI instanciado no arquivo backend/core/agent.py:

```Python
base_url='[https://llm.liaufms.org/v1/gemma-3-12b-it](https://llm.liaufms.org/v1/gemma-3-12b-it)'
api_key='Sua_Chave_Aqui'
model='google/gemma-3-12b-it'
```
## Banco de dados
O SQLite usado pelo sistema cria o arquivo automaticamente na raiz do backend:

```
backend/db/jarvis.db
```
Para forçar a criação do banco de dados vazio e de suas tabelas, execute:

```Bash
python backend/core/database.py
```
Consultar o banco diretamente via terminal:

```Bash
sqlite3 backend/db/jarvis.db
```






