# Trabalho-IA-Jarvis

Assistente acadêmico com chat, RAG sobre PDFs, gerenciamento de tarefas, agenda e logs de observabilidade via Tool Calling.

## Stack

- Frontend: Streamlit
- Backend: Python 3.10
- IA: Cliente OpenAI-compatible (Qwen/Qwen2.5-14B-Instruct-AWQ)
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
base_url='[https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq](https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq)'
api_key='Sua_Chave'
model='Qwen/Qwen2.5-14B-Instruct-AWQ'
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
│   │   ├── learning.py    # Lógica de geração de resumos e perguntas de Active Recall
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

## Modo Aprendizado (learning.py)

O módulo de aprendizado oferece funcionalidades educativas baseadas nos documentos indexados pelo RAG, acessíveis pela barra lateral da interface.

### Funcionalidades

**1. Active Recall**

Gera automaticamente uma pergunta desafiadora sobre um tópico escolhido pelo usuário, com base exclusivamente nos PDFs da pasta `data/`. O fluxo é:

1. O usuário digita um tópico na sidebar
2. O sistema busca trechos relevantes no índice FAISS via `buscar_trechos_relevantes()`
3. É formulado uma pergunta de Active Recall sem revelar a resposta
4. O usuário responde e solicita a avaliação

**2. Guia de Revisão**

Gera um guia estruturado sobre o tópico contendo:
- Os 3 conceitos principais a serem lembrados
- As "pegadinhas" e partes mais difíceis do tema
- Uma recomendação prática de como aplicar o conteúdo

### Limitações

- Todas as funcionalidades dependem do RAG: se nenhum PDF relevante ao tópico estiver na pasta `data/`, o sistema retorna uma mensagem de aviso em vez de inventar conteúdo
- O guia de revisão (`gerar_guia_revisao`) está implementado no backend mas ainda não está exposto na interface Streamlit

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
