# Arquitetura da Aplicação Django para o Observatório de IA

Este documento descreve a arquitetura proposta para a aplicação Django do Observatório de IA, incorporando gestão de conhecimento, Graph RAG e LLMs locais, com base nos requisitos levantados e nas tecnologias pesquisadas.

## 1. Visão Geral

A aplicação será uma plataforma web construída com Django, projetada para ser modular e extensível. Ela integrará funcionalidades de gestão de informações, processamento de documentos, construção de grafo de conhecimento, consulta via RAG (Retrieval-Augmented Generation) baseada em grafo (Graph RAG) e colaboração.

## 2. Componentes Principais

A arquitetura será composta pelos seguintes módulos principais:

*   **Core (Django App):** Gerencia a lógica central da aplicação, modelos de dados relacionais, autenticação, permissões e a interface web principal.
*   **Gestão de Fontes (Django App):** Responsável pelo cadastro, categorização e monitoramento das fontes de informação (sites, feeds RSS, APIs, etc.).
*   **Processamento de Documentos (Módulo Python/Celery Task):** Lida com o carregamento (manual/automático), parsing (PDF, DOCX, web), extração de metadados/entidades/relações e pré-processamento de texto.
*   **Base de Conhecimento Relacional (PostgreSQL/SQLite):** Armazena metadados de usuários, fontes, documentos, tarefas, newsletters, comentários, etc., gerenciados pelo ORM do Django.
*   **Base de Conhecimento em Grafo (Memgraph):** Armazena as entidades e relacionamentos extraídos dos documentos, formando o grafo de conhecimento. Escolhido por performance in-memory, suporte a Python (MAGE) e Cypher.
*   **Indexação Vetorial (FAISS/LlamaIndex):** Cria e gerencia índices vetoriais dos chunks de texto dos documentos para a etapa de recuperação do RAG.
*   **Graph RAG (LlamaIndex/Langchain):** Orquestra o processo de consulta: recebe a pergunta do usuário, consulta o grafo de conhecimento (Memgraph) e/ou o índice vetorial (FAISS), recupera informações relevantes e utiliza o LLM local para gerar a resposta.
*   **LLM Local (Ollama + IBM Granite/Outros):** Serve o Large Language Model (LLM) localmente via Ollama, recebendo prompts do componente Graph RAG e gerando texto (respostas, sumarizações, extrações).
*   **Interface do Usuário (Django Templates/HTMX + JS):** Fornece a interface web para interação do usuário, incluindo dashboards, formulários de cadastro, visualização de documentos, interface de consulta RAG e visualização do grafo (usando libs como vis.js ou d3.js).
*   **Gestão de Tarefas (Celery + Redis/RabbitMQ):** Executa tarefas assíncronas em background, como scraping de fontes, processamento de documentos, indexação e envio de newsletters.
*   **Newsletter (Django App + Celery):** Gerencia o cadastro de assinantes e a criação/envio de newsletters com base nas atualizações da base de conhecimento.
*   **Colaboração (Django App):** Implementa funcionalidades como comentários em documentos, notas compartilhadas e controle de acesso.

## 3. Fluxo de Dados e Interações

1.  **Ingestão:**
    *   Fontes são cadastradas (manualmente ou via descoberta).
    *   Tarefas (Celery) monitoram fontes ou recebem uploads manuais.
    *   Documentos são baixados/recebidos.
    *   O módulo de Processamento (Celery) parseia o documento, extrai texto e metadados.
    *   Metadados são salvos no DB Relacional (PostgreSQL).
    *   Texto é dividido em chunks.
    *   Chunks são enviados para o LLM (via GraphRAGExtractor/Langchain) para extração de entidades/relações.
    *   Entidades/Relações são salvas no Grafo (Memgraph).
    *   Chunks são vetorizados e salvos no Índice Vetorial (FAISS).
2.  **Consulta (Graph RAG):**
    *   Usuário envia pergunta via Interface Web.
    *   O componente Graph RAG (LlamaIndex) recebe a pergunta.
    *   Consulta o Grafo (Memgraph) para entidades/relações relevantes e/ou o Índice Vetorial (FAISS) para chunks de texto similares.
    *   Constrói um prompt enriquecido com o contexto recuperado.
    *   Envia o prompt para o LLM Local (Ollama).
    *   Recebe a resposta gerada pelo LLM.
    *   Apresenta a resposta ao usuário na Interface Web.
3.  **Outras Funcionalidades:**
    *   Usuários interagem com a interface para gerenciar fontes, tarefas, usuários, etc.
    *   Funcionalidades colaborativas permitem adicionar comentários/notas associadas aos documentos/entidades.
    *   Tarefas (Celery) geram e enviam newsletters periodicamente.

## 4. Tecnologias Propostas

*   **Backend:** Python 3.10+, Django 5+
*   **Banco de Dados Relacional:** PostgreSQL (produção), SQLite (desenvolvimento)
*   **Banco de Dados de Grafo:** Memgraph
*   **LLM Serving:** Ollama
*   **LLM:** IBM Granite (inicialmente, explorando outros modelos quantizados compatíveis com 8GB VRAM)
*   **Graph RAG / Indexing:** LlamaIndex, Langchain, FAISS
*   **Processamento de Documentos:** PyMuPDF (ou pypdf), python-docx, BeautifulSoup4 (para HTML)
*   **Task Queue:** Celery, Redis (ou RabbitMQ)
*   **Frontend:** Django Templates, HTMX (para interatividade dinâmica), JavaScript (para visualização de grafo - vis.js/d3.js)
*   **Containerização (Opcional):** Docker, Docker Compose

## 5. Próximos Passos

Com a arquitetura definida, o próximo passo é configurar o ambiente de desenvolvimento e começar a implementação dos modelos de dados base no Django.
