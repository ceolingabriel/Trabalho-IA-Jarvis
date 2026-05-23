
## Dataset

Os documentos utilizados para alimentar o sistema RAG estão na pasta `backend/data/`. São 12 artigos científicos em inglês, cobrindo os temas centrais do projeto: agentes com LLMs, tool calling, RAG, otimização de compiladores com IA e geração de código.

### Configuração de Chunking

Os documentos são processados automaticamente ao iniciar o sistema com os seguintes parâmetros definidos em `backend/core/rag.py`:

- **Tamanho do chunk:** 800 caracteres
- **Overlap:** 150 caracteres
- **Estratégia:** `RecursiveCharacterTextSplitter` (LangChain)
- **Embeddings:** `all-MiniLM-L6-v2` via sentence-transformers (indexado com FAISS)

### Documentos

| Arquivo | Título | Tipo | Origem | Limitações |
|---|---|---|---|---|
| `1901.05719v2.pdf` | AI Coding: Learning to Construct Error Correction Codes | Artigo científico | [ArXiv (cs.IT)](https://arxiv.org/abs/1901.05719) | Inglês; foco restrito a códigos de correção de erros |
| `2104.05573v1.pdf` | AI Powered Compiler Techniques for DL Code Optimization | Artigo científico | [ArXiv (cs.PL)](https://arxiv.org/abs/2104.05573) | Inglês; escopo restrito a CPUs e primitivas de deep learning |
| `2409.18807v1.pdf` | LLM With Tools: A Survey | Survey | [ArXiv (cs.AI)](https://arxiv.org/abs/2409.18807) | Inglês; conhecimento limitado à data de publicação (set/2024) |
| `2601.12146v2.pdf` | From LLMs to Agents in Programming: The Impact of Providing an LLM with a Compiler | Artigo científico | [ArXiv (cs.SE)](https://arxiv.org/abs/2601.12146) | Inglês; testes restritos à linguagem C e dataset RosettaCode |
| `2025.acl-long.103.pdf` | *(artigo ACL 2025)* | Artigo de conferência | ACL Anthology (ACL 2025) | Inglês; acesso restrito ao conteúdo da conferência |
| `3660810.pdf` | *(artigo ACM)* | Artigo de conferência | ACM Digital Library | Inglês; pode exigir acesso institucional para verificação |
| `3661167.3661221.pdf` | A Performance Study of LLM-Generated Code on Leetcode | Artigo de conferência | [ACM — EASE 2024](https://dl.acm.org/doi/10.1145/3661167.3661221) | Inglês; dataset limitado ao LeetCode; risco de data contamination |
| `3706598.3714008.pdf` | The Impact of Generative AI Coding Assistants on Developers Who Are Visually Impaired | Artigo de conferência | [ACM — CHI 2025](https://dl.acm.org/doi/10.1145/3706598.3714008) | Inglês; escopo restrito a desenvolvedores com deficiência visual |
| `3725843.3756064.pdf` | Elk: Exploring the Efficiency of Inter-core Connected AI Chips with Deep Learning Compiler Techniques | Artigo de conferência | [ACM — MICRO 2025](https://doi.org/10.1145/3725843.3756064) | Inglês; foco em hardware específico (chips ICCA/IPU) |
| `AdvancementsinAI-BasedCompilerOptimization(...).pdf` | Advancements in AI-Based Compiler Optimization Techniques for Machine Learning Workloads | Artigo científico | [Publicação acadêmica](https://www.researchgate.net/profile/Vasuki-Sb/publication/390572199_Advancements_in_AI-Based_Compiler_Optimization_Techniques_for_Machine_Learning_Workloads/links/67f4acdb49e91c0feae9ed49/Advancements-in-AI-Based-Compiler-Optimization-Techniques-for-Machine-Learning-Workloads.pdf) | Inglês; escopo restrito a otimização de compiladores para ML |
| `Information Systems Journal - 2025 - Pieper (...).pdf` | How AI Helps to Compile Human Intelligence: An Empirical Study of Emerging... | Artigo de journal | [Information Systems Journal (2025)](https://onlinelibrary.wiley.com/doi/full/10.1111/isj.12585) | Inglês; acesso via assinatura institucional |
| `s00259-023-06172-w.pdf` | *(artigo)* | Artigo científico | Publicação indexada | Inglês; verificar acesso via DOI original |
