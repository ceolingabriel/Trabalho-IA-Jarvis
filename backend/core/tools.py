import os
import json
from datetime import datetime
from backend.core import database as db
from backend.core.rag import JarvisRAG

rag_system = JarvisRAG()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'tool_calls.log')

FERRAMENTAS_JARVIS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_agenda",
            "description": "Consulta a agenda acadêmica para uma data (YYYY-MM-DD).",
            "parameters": {"type": "object", "properties": {"data": {"type": "string"}}, "required": ["data"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista tarefas pendentes ou concluídas.",
            "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["pendente", "concluída"]}}, "required": ["status"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona nova tarefa.",
            "parameters": {"type": "object", "properties": {"descricao": {"type": "string"}, "data_limite": {"type": "string"}}, "required": ["descricao", "data_limite"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "concluir_tarefa",
            "description": "Conclui tarefa pelo ID.",
            "parameters": {"type": "object", "properties": {"tarefa_id": {"type": "integer"}}, "required": ["tarefa_id"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_material_rag",
            "description": "Busca resumos e conceitos nos PDFs de estudo.",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        }
    }
]

def executar_ferramenta(nome: str, argumentos: dict) -> str:
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Ferramenta: {nome} | Entrada: {argumentos}\n")
        
    if nome == "consultar_agenda": return db.consultar_agenda(argumentos["data"])
    elif nome == "listar_tarefas": return db.listar_tarefas(argumentos["status"])
    elif nome == "adicionar_tarefa": return db.adicionar_tarefa(argumentos["descricao"], argumentos["data_limite"])
    elif nome == "concluir_tarefa": return db.concluir_tarefa(argumentos["tarefa_id"])
    elif nome == "buscar_material_rag": return rag_system.buscar_trechos_relevantes(argumentos["query"])
    return "Ferramenta não encontrada."