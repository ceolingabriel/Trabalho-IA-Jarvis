import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'jarvis.db')

def _conectar():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 3.2
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT
        )
    ''')
    # 3.3
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data_limite TEXT,
            status TEXT DEFAULT 'pendente'
        )
    ''')
    conn.commit()
    return conn

# --3.2--
def consultar_agenda(data: str) -> str:
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT horario, titulo, tipo FROM agenda WHERE data = ? ORDER BY horario", (data,))
        eventos = cursor.fetchall()
        conn.close()
        if not eventos: return f"A agenda está livre para o dia {data}."
        
        resultado = f"Agenda para {data}:\n"
        for horario, titulo, tipo in eventos:
            resultado += f"- [{tipo.upper()}] {horario}: {titulo}\n"
        return resultado
    except Exception as e: return f"Erro na agenda: {e}"

# --3.3--
def adicionar_tarefa(descricao: str, data_limite: str) -> str:
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tarefas (descricao, data_limite) VALUES (?, ?)", (descricao, data_limite))
        conn.commit()
        conn.close()
        return f"Tarefa '{descricao}' adicionada para {data_limite}."
    except Exception as e: return f"Erro ao adicionar tarefa: {e}"

def listar_tarefas(status: str = "pendente") -> str:
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descricao, data_limite FROM tarefas WHERE status = ?", (status,))
        tarefas = cursor.fetchall()
        conn.close()
        if not tarefas: return f"Nenhuma tarefa '{status}' encontrada."
        
        resultado = f"Tarefas {status}s:\n"
        for tid, desc, limite in tarefas:
            resultado += f"[ID: {tid}] {desc} (Prazo: {limite})\n"
        return resultado
    except Exception as e: return f"Erro ao listar: {e}"

def concluir_tarefa(tarefa_id: int) -> str:
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET status = 'concluída' WHERE id = ?", (tarefa_id,))
        conn.commit()
        conn.close()
        return f"Tarefa {tarefa_id} concluída com sucesso."
    except Exception as e: return f"Erro ao concluir: {e}"

if __name__ == "__main__":
    print("Iniciando a criação do banco de dados...")
    _conectar()
    resultado = adicionar_tarefa("Estudar Inteligência Artificial", "2026-05-25")
    print(resultado)
    print("Banco jarvis.db criado com sucesso na pasta db!")