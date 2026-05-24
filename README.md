# Trabalho-IA-Jarvis

Assistente acadêmico com chat, RAG sobre PDFs, gerenciamento de tarefas, agenda e logs de observabilidade via Tool Calling.

## Stack

- Frontend: Streamlit
- Backend: Python 3.10
- IA: Cliente OpenAI-compatible (google/gemma-3-12b-it)
- Banco: SQLite (Nativo)
- RAG: FAISS + sentence-transformers (all-MiniLM-L6-v2)
- Runtime: Ambiente Virtual Isolado (venv)

## Executar Localmente

### Pré-requisitos
* Ter o [Git](https://git-scm.com/) instalado.
* Ter o [Python 3.10 ou superior](https://www.python.org/downloads/) instalado globalmente na máquina.

### Passo a Passo de Instalação
Ative o ambiente do projeto:

```python
python -m venv .venv
```
Ative a bolha de isolamento de acordo com o seu sistema operacional:

Windows (Prompt de Comando ou PowerShell):

```Bash
.venv\Scripts\activate
``` 
Linux / Mac (Terminal):

```Bash
source .venv/bin/activate
```
O terminal exibirá o prefixo (.venv) confirmando a ativação bem-sucedida.


## Instale o PyTorch + dependências
Para evitar o download desnecessário de pacotes gigantescos contendo drivers de placas de vídeo (CUDA), force a instalação da versão leve específica para execução em processadores comuns:

```Bash
pip install torch torchvision --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
```

```Bash
pip install -r requirements.txt
```
Inicialize o Banco de Dados:

```Bash
python backend/core/database.py
```


## Inicie o Assistente Visual
Suba o frontend e o backend simultaneamente:
```python
streamlit run frontend/app.py
```
Acesse:

```Plaintext
Frontend: http://localhost:8501
```
O terminal exibirá os logs de execução do Streamlit. Para parar a aplicação, pressione Ctrl + C no terminal.

## Configuração da LLM
As chaves e os endpoints estão configurados diretamente no cliente OpenAI instanciado no arquivo backend/core/agent.py:

```python
base_url='[https://llm.liaufms.org/v1/gemma-3-12b-it](https://llm.liaufms.org/v1/gemma-3-12b-it)'
api_key='Sua_Chave'
model='google/gemma-3-12b-it'
```
## Banco de dados
O SQLite usado pelo sistema cria o arquivo automaticamente na raiz do backend:

```python
backend/db/jarvis.db
```
Consultar o banco diretamente via terminal:

```python
sqlite3 backend/db/jarvis.db
```
## Logs de Observabilidade
A cada chamada de ferramenta feita pela IA, o sistema grava automaticamente o evento, a entrada e a saída de dados.

Os logs persistem em:

```python
backend/logs/tool_calls.log
```


## Estrutura de Pastas
```markdown
Trabalho-IA-Jarvis/
├── backend/
│   ├── core/
│   │   ├── agent.py       # Lógica principal do agente ReAct
│   │   ├── database.py    # SQLite: agenda e tarefas
│   │   ├── rag.py         # Indexação e busca FAISS
│   │   └── tools.py       # Roteador de ferramentas + logs
│   ├── data/              # PDFs indexados pelo RAG
│   ├── db/                # jarvis.db (criado automaticamente)
│   └── logs/              # tool_calls.log (criado automaticamente)
└── frontend/
└── app.py             # Interface Streamlit
```
## Ferramentas Disponíveis

| Ferramenta | O que faz |
|---|---|
| `consultar_agenda` | Retorna eventos de um dia específico |
| `listar_tarefas` | Lista tarefas pendentes ou concluídas |
| `adicionar_tarefa` | Cria nova tarefa com prazo |
| `concluir_tarefa` | Marca tarefa como concluída pelo ID |
| `buscar_material_rag` | Busca semântica nos PDFs da pasta `data/` |


## Arquitetura

O agente segue o padrão **ReAct** (Reasoning + Acting): o usuário envia uma mensagem → o agente decide se precisa usar uma ferramenta → executa a ferramenta → usa o resultado para formular a resposta final. Toda chamada de ferramenta é registrada automaticamente em `backend/logs/tool_calls.log`.


## Limitações Conhecidas

- O modelo pode ocasionalmente retornar JSON mal formatado ao tentar chamar uma ferramenta. O sistema trata esse erro automaticamente e solicita que o usuário repita a pergunta.
- O índice FAISS é construído em memória a cada inicialização — quanto mais PDFs na pasta `data/`, maior o tempo de startup.

## IAs Utilizadas

| Ferramenta | Uso |
|---|---| 
| `Claude (Anthropic)` | Auxílio na arquitetura e revisão do código, e documentação |
| `Gemini (Google)` | Auxílio na construção da arquitetura |
