import json
from datetime import datetime
from openai import OpenAI
from backend.core.tools import executar_ferramenta

client = OpenAI(
    base_url='https://llm.liaufms.org/v1/gemma-3-12b-it', 
    api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A'
)

def interagir_com_jarvis(mensagem_usuario: str, historico: list = None) -> str:
    if historico is None:
        historico = []
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # 1. ENGENHARIA DE PROMPT (ReAct) Mais Rigorosa
    prompt_sistema = f"""Você é o JARVIS, um assistente acadêmico autônomo. Hoje é {hoje}.
Você possui as seguintes ferramentas:
- consultar_agenda (parâmetro: "data" em formato YYYY-MM-DD)
- listar_tarefas (parâmetro: "status" podendo ser "pendente" ou "concluída")
- adicionar_tarefa (parâmetros: "descricao", "data_limite" em YYYY-MM-DD)
- concluir_tarefa (parâmetro: "tarefa_id" em número inteiro)
- buscar_material_rag (parâmetro: "query" em string)

REGRA DE OURO: Se precisar usar uma ferramenta, retorne APENAS um JSON puro, SEM MARKDOWN, SEM EXPLICAÇÕES ANTES OU DEPOIS. 
Exemplo exato e obrigatório do que você deve retornar:
{{"tool": "listar_tarefas", "args": {{"status": "pendente"}}}}

Se não precisar de ferramenta, responda normalmente em texto."""
        
    mensagens = [{"role": "system", "content": prompt_sistema}] + historico
    mensagens.append({"role": "user", "content": mensagem_usuario})

    resposta = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=mensagens,
        temperature=0.1
    )
    
    texto_resposta = resposta.choices[0].message.content
    
    if '{"tool"' in texto_resposta or '{"tool":' in texto_resposta:
        try:
            
            texto_limpo = texto_resposta.replace('```json', '').replace('```', '').strip()
            
            
            inicio = texto_limpo.find('{')
            fim = texto_limpo.rfind('}') + 1
            json_str = texto_limpo[inicio:fim]
            
            dados_ferramenta = json.loads(json_str)
            nome_ferramenta = dados_ferramenta.get("tool")
            args_ferramenta = dados_ferramenta.get("args", {})
            
            
            resultado = executar_ferramenta(nome_ferramenta, args_ferramenta)
            
            
            mensagens.append({"role": "assistant", "content": json_str})
            mensagens.append({"role": "user", "content": f"O sistema retornou estes dados: {resultado}. Com base neles, responda à minha pergunta."})
            
            resposta_final = client.chat.completions.create(
                model='google/gemma-3-12b-it',
                messages=mensagens,
                temperature=0.3
            )
            return resposta_final.choices[0].message.content
            
        except Exception as e:
            
            print(f"\n[ERRO DE PARSER] O texto original da IA foi:\n{texto_resposta}")
            print(f"[ERRO DE PARSER] A falha do Python foi: {e}\n")
            return "Desculpe, a IA tentou formatar os dados de busca, mas cometeu um erro de sintaxe. Pode perguntar de novo?"

    
    return texto_resposta