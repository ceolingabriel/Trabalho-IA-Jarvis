
## Dataset

Os documentos utilizados para alimentar o sistema RAG estão na pasta `backend/data/`. São 12 artigos científicos em inglês, cobrindo os temas centrais do projeto: agentes com LLMs, tool calling, RAG, otimização de compiladores com IA e geração de código.

### Configuração de Chunking

Os documentos são processados automaticamente ao iniciar o sistema com os seguintes parâmetros definidos em `backend/core/rag.py`:

- **Tamanho do chunk:** 800 caracteres
- **Overlap:** 150 caracteres
- **Estratégia:** `RecursiveCharacterTextSplitter` (LangChain)
- **Escopo:** global (todos os PDFs tratados como um único texto)
- **Embeddings:** `all-MiniLM-L6-v2` via sentence-transformers (indexado com FAISS)

### Documentos

| Arquivo | Título | Tipo | Origem | Limitações |
|---|---|---|---|---|
| `1901.05719v2.pdf` | AI Coding: Learning to Construct Error Correction Codes | Artigo científico | [ArXiv (cs.IT)](https://arxiv.org/abs/1901.05719) | Layout de duas colunas causa quebras de palavras na extração (ex: `COMMUNICA TIONS`, `OCTOBE R`); notação matemática e tabelas de algoritmos são extraídas como texto desorganizado |
| `2104.05573v1.pdf` | AI Powered Compiler Techniques for DL Code Optimization | Artigo científico | [ArXiv (cs.PL)](https://arxiv.org/abs/2104.05573) | Gráficos de desempenho e figuras são perdidos na extração; páginas com resultados visuais geram chunks com poucos caracteres e baixa densidade informacional |
| `2409.18807v1.pdf` | LLM With Tools: A Survey | Survey | [ArXiv (cs.AI)](https://arxiv.org/abs/2409.18807) | Tabelas de resultados são extraídas como texto plano sem alinhamento, dificultando a interpretação dos dados pelo RAG |
| `2601.12146v2.pdf` | From LLMs to Agents in Programming: The Impact of Providing an LLM with a Compiler | Artigo científico | [ArXiv (cs.SE)](https://arxiv.org/abs/2601.12146) | Documento mais longo; trechos de código e métricas ROUGE podem ser fragmentados entre chunks, perdendo contexto |
| `2025.acl-long.103.pdf` | CompileAgent: Automated Real-World Repo-Level Compilation with Tool-Integrated LLM-based Agent System | Artigo de conferência | [ACL Anthology (ACL 2025)](https://aclanthology.org/2025.acl-long.103/) | Tabelas com símbolos especiais e dados de benchmark são extraídas de forma fragmentada; última página tem densidade muito baixa |
| `3660810.pdf` | ClarifyGPT: A Framework for Enhancing LLM-Based Code Generation via Requirements Clarification | Artigo de conferência | [ACM Digital Library](https://dl.acm.org/doi/full/10.1145/3660810) | Documento longo; maior risco de diluição no corpus global; cabeçalhos repetidos em todas as páginas geram ruído nos chunks |
| `3661167.3661221.pdf` | A Performance Study of LLM-Generated Code on Leetcode | Artigo de conferência | [ACM — EASE 2024](https://dl.acm.org/doi/10.1145/3661167.3661221) | Figuras com gráficos de coeficiente de variação não são extraíveis; chunks da seção de resultados podem conter apenas rótulos de eixos sem contexto |
| `3706598.3714008.pdf` | The Impact of Generative AI Coding Assistants on Developers Who Are Visually Impaired | Artigo de conferência | [ACM — CHI 2025](https://dl.acm.org/doi/10.1145/3706598.3714008) | Documento longo com muito conteúdo qualitativo; última página extraída com apenas 204 chars, indicando perda de conteúdo no final do PDF |
| `3725843.3756064.pdf` | Elk: Exploring the Efficiency of Inter-core Connected AI Chips with Deep Learning Compiler Techniques | Artigo de conferência | [ACM — MICRO 2025](https://doi.org/10.1145/3725843.3756064) | PDF mais pesado do dataset (4MB, 106k chars); alto volume de diagramas de arquitetura e pseudocódigo que não são extraíveis pelo pypdf |
| `AdvancementsinAI-BasedCompilerOptimization(...).pdf` | Advancements in AI-Based Compiler Optimization Techniques for Machine Learning Workloads | Artigo científico | [Research Gate](https://www.researchgate.net/publication/390572199_Advancements_in_AI-Based_Compiler_Optimization_Techniques_for_Machine_Learning_Workloads) | Cabeçalhos de rodapé do journal repetidos em todas as páginas geram ruído constante nos chunks |
| `Information Systems Journal - 2025 - Pieper (...).pdf` | How AI Helps to Compile Human Intelligence: An Empirical Study of Emerging... | Artigo de journal | [Information Systems Journal (2025)](https://onlinelibrary.wiley.com/doi/full/10.1111/isj.12585) | Documento mais denso do dataset (23 págs, 150k chars); maior contribuição proporcional ao corpus global, podendo sobrepor temas dos outros documentos |
| `s00259-023-06172-w.pdf` | Large language models (LLM) and ChatGPT: what will the impact on nuclear medicine be? | Artigo científico | [Springer Nature Link](https://link.springer.com/article/10.1007/s00259-023-06172-w) | Documento muito curto; escopo restrito a medicina nuclear, tema distante dos demais artigos do dataset; caracteres especiais presentes na extração |
