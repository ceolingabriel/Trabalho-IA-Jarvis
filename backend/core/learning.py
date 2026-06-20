from backend.core.agent import client
from backend.core.tools import rag_system

# =================================================================
# FUNCIONALIDADE 1: ACTIVE RECALL (INTERATIVA - OBRIGATÓRIA)
# =================================================================
def gerar_exercicio_active_recall(topico: str) -> str:
    """Usa o RAG para ler o material e gera uma pergunta interativa para o aluno."""
    contexto = rag_system.buscar_trechos_relevantes(topico, top_k=6)
    
    if "Nenhum material" in contexto:
        return "Adicione documentos sobre este tópico na pasta data/ primeiro!"
        
    prompt = (
        "Baseado EXCLUSIVAMENTE neste contexto dos materiais do aluno:\n"
        f"{contexto}\n\n"
        "Gere UMA pergunta desafiadora de Active Recall para testar o conhecimento dele sobre o tópico. "
        "Não dê a resposta. Retorne APENAS a pergunta, sem introduções, sem explicações e sem repetir o contexto."
    )
    
    resposta = client.chat.completions.create(
        model='Qwen/Qwen2.5-14B-Instruct-AWQ',
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

def avaliar_resposta_aluno(pergunta: str, resposta_aluno: str, topico: str) -> str:
    """Avalia se a resposta do aluno está correta com base no material base."""
    contexto = rag_system.buscar_trechos_relevantes(topico)
    
    prompt = (
        f"Material de Referência:\n{contexto}\n\n"
        f"Pergunta feita: {pergunta}\n"
        f"Resposta do aluno: {resposta_aluno}\n\n"
        "Avalie criticamente a resposta do aluno. Diga se está correta, parcialmente correta ou incorreta. "
        "Justifique apontando o que faltou ou o que está certo com base no Material de Referência."
    )
    
    resposta = client.chat.completions.create(
        model='Qwen/Qwen2.5-14B-Instruct-AWQ',
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

# =================================================================
# FUNCIONALIDADE 2: RECOMENDAÇÃO DE REVISÃO
# =================================================================
def gerar_guia_revisao(topico: str) -> str:
    """Lê o RAG e identifica os pontos principais e dificuldades para o aluno focar."""
    contexto = rag_system.buscar_trechos_relevantes(topico)
    
    if "Nenhum material" in contexto:
        return "Adicione documentos sobre este tópico na pasta data/ primeiro!"
        
    prompt = (
        f"Material de Referência:\n{contexto}\n\n"
        f"O aluno precisa revisar o tópico: '{topico}'. "
        "Crie um guia de revisão rápido contendo:\n"
        "1. Os 3 conceitos principais a serem lembrados (resumo curto).\n"
        "2. Identificação de dificuldades: Quais são as 'pegadinhas' ou partes mais difíceis desse tema?\n"
        "3. Uma recomendação de como aplicar isso."
    )
    
    resposta = client.chat.completions.create(
        model='Qwen/Qwen2.5-14B-Instruct-AWQ',
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content
