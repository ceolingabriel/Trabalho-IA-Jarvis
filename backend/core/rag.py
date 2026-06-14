# backend/core/rag.py
import os
import glob
import numpy as np
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

class JarvisRAG:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len
        )
        self.index = None
        self.chunks = []
        self.carregar_documentos_locais()

    def ler_pdf(self, caminho_arquivo: str) -> str:
        """Extrai texto de um arquivo PDF."""
        texto = ""
        try:
            leitor = PdfReader(caminho_arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
        except Exception as e:
            print(f"[RAG] Erro ao ler PDF {caminho_arquivo}: {e}")
        return texto

    def carregar_documentos_locais(self):
        """Lê todos os PDFs e TXTs da pasta data/ e indexa no FAISS."""
        os.makedirs(DATA_DIR, exist_ok=True)
        arquivos = glob.glob(os.path.join(DATA_DIR, "*.*"))
        
        texto_completo = ""
        for arquivo in arquivos:
            if arquivo.endswith('.pdf'):
                texto_completo += self.ler_pdf(arquivo)
            elif arquivo.endswith('.txt'):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    texto_completo += f.read() + "\n"
                    
        if texto_completo.strip():
            self._indexar_texto(texto_completo)
            print(f"[RAG] Carregados e indexados {len(arquivos)} documentos da pasta data/.")
        else:
            print("[RAG] Aviso: Nenhum documento encontrado na pasta data/.")

    def _indexar_texto(self, texto: str):
        novos_chunks = self.text_splitter.split_text(texto)
        self.chunks.extend(novos_chunks)
        embeddings = self.embedding_model.encode(novos_chunks)
        
        dimensao = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimensao)
            
        self.index.add(np.array(embeddings).astype('float32'))

    def buscar_trechos_relevantes(self, query: str, top_k: int = 6) -> str:
        """Retorna os trechos mais relevantes combinados em uma única string."""
        if self.index is None or len(self.chunks) == 0:
            return "Nenhum material de estudo encontrado. O dataset está vazio."
            
        query_embedding = self.embedding_model.encode([query])
        distancias, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        trechos = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                trechos.append(self.chunks[idx])
                
        return "\n...\n".join(trechos)
