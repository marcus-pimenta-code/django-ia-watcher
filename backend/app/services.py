# rag_integration/services.py

import logging
from django.conf import settings
from llama_index.core import ( # Updated imports
    StorageContext,
    VectorStoreIndex,
    KnowledgeGraphIndex,
    Settings,
)
from llama_index.core.graph_stores import SimpleGraphStore # Using SimpleGraphStore initially
from llama_index.core.vector_stores import SimpleVectorStore # Using SimpleVectorStore initially
# from llama_index.graph_stores.memgraph import MemgraphGraphStore # Keep for later Memgraph integration
# from llama_index.vector_stores.faiss import FaissVectorStore # Keep for later Faiss integration
# import faiss # Keep for later Faiss integration

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from documentos.models import Document, DocumentChunk

logger = logging.getLogger(__name__)

# --- Configuration (Consider moving to Django settings) ---
MEMGRAPH_HOST = settings.MEMGRAPH_HOST if hasattr(settings, "MEMGRAPH_HOST") else "localhost"
MEMGRAPH_PORT = settings.MEMGRAPH_PORT if hasattr(settings, "MEMGRAPH_PORT") else 7687
OLLAMA_BASE_URL = settings.OLLAMA_BASE_URL if hasattr(settings, "OLLAMA_BASE_URL") else "http://localhost:11434"
LLM_MODEL_NAME = settings.LLM_MODEL_NAME if hasattr(settings, "LLM_MODEL_NAME") else "ibm/granite-code-8b" # Or another model compatible with user's hardware
EMBEDDING_MODEL_NAME = settings.EMBEDDING_MODEL_NAME if hasattr(settings, "EMBEDDING_MODEL_NAME") else "nomic-embed-text" # Default Ollama embedding model
# FAISS_INDEX_PATH = settings.FAISS_INDEX_PATH if hasattr(settings, "FAISS_INDEX_PATH") else "/path/to/faiss_index.bin" # Define path for Faiss

# --- Initialization --- (Could be cached or made into singletons)

def get_llm():
    """Initializes and returns the Ollama LLM."""
    return Ollama(model=LLM_MODEL_NAME, base_url=OLLAMA_BASE_URL, request_timeout=120.0) # Increased timeout

def get_embedding_model():
    """Initializes and returns the Ollama Embedding model."""
    return OllamaEmbedding(model_name=EMBEDDING_MODEL_NAME, base_url=OLLAMA_BASE_URL)

def get_graph_store():
    """Initializes and returns the Graph Store."""
    # TODO: Switch to MemgraphGraphStore when Memgraph is set up
    # return MemgraphGraphStore(host=MEMGRAPH_HOST, port=MEMGRAPH_PORT)
    logger.warning("Using SimpleGraphStore for initial development.")
    return SimpleGraphStore()

def get_vector_store():
    """Initializes and returns the Vector Store."""
    # TODO: Switch to FaissVectorStore when Faiss is set up
    # try:
    #     index = faiss.read_index(FAISS_INDEX_PATH)
    #     return FaissVectorStore(faiss_index=index)
    # except Exception as e:
    #     logger.warning(f"Could not load Faiss index from {FAISS_INDEX_PATH}: {e}. Creating new in-memory index.")
    #     # Define FAISS index dimensions based on embedding model
    #     # d = get_embedding_model().embed_dim # Need to get dimension
    #     d = 768 # Example dimension for nomic-embed-text, adjust as needed
    #     index = faiss.IndexFlatL2(d)
    #     return FaissVectorStore(faiss_index=index)
    logger.warning("Using SimpleVectorStore for initial development.")
    return SimpleVectorStore()

def setup_llama_index_settings():
    """Sets up global LlamaIndex settings for LLM and Embedding model."""
    Settings.llm = get_llm()
    Settings.embed_model = get_embedding_model()

# --- Indexing --- (Likely called from Celery tasks)

def build_indices_for_document(document_id):
    """Builds/updates graph and vector indices for a given document."""
    setup_llama_index_settings() # Ensure settings are configured
    try:
        doc = Document.objects.get(id=document_id)
        if not doc.extracted_text:
            logger.warning(f"Document {document_id} has no extracted text. Skipping indexing.")
            return

        # Create LlamaIndex Document object from extracted text
        # We might want to use DocumentChunk models later for more granularity
        from llama_index.core import Document as LlamaDocument
        llama_doc = LlamaDocument(text=doc.extracted_text, doc_id=str(doc.id), extra_info={"title": doc.title})

        # Get stores
        graph_store = get_graph_store()
        vector_store = get_vector_store()
        storage_context = StorageContext.from_defaults(graph_store=graph_store, vector_store=vector_store)

        # Build Knowledge Graph Index
        # This will extract triplets and add them to the graph store
        logger.info(f"Building Knowledge Graph Index for document {document_id}...")
        kg_index = KnowledgeGraphIndex.from_documents(
            [llama_doc],
            storage_context=storage_context,
            max_triplets_per_chunk=10,
            include_embeddings=True, # Include embeddings for graph RAG
            show_progress=True,
        )
        logger.info(f"Finished building Knowledge Graph Index for document {document_id}.")

        # Build Vector Store Index (implicitly uses the same storage context)
        # logger.info(f"Building Vector Store Index for document {document_id}...")
        # vector_index = VectorStoreIndex.from_documents(
        #     [llama_doc],
        #     storage_context=storage_context,
        #     show_progress=True,
        # )
        # logger.info(f"Finished building Vector Store Index for document {document_id}.")

        # TODO: Persist stores if needed (e.g., save FAISS index)
        # if isinstance(vector_store, FaissVectorStore):
        #     vector_store.persist(persist_path=FAISS_INDEX_PATH)

        logger.info(f"Successfully updated indices for document {document_id}.")

    except Document.DoesNotExist:
        logger.error(f"Document {document_id} not found for indexing.")
    except Exception as e:
        logger.error(f"Error building indices for document {document_id}: {e}", exc_info=True)

# --- Querying --- (Called from Django views)

def query_knowledge_base(query_text):
    """Queries the knowledge base using Graph RAG."""
    setup_llama_index_settings()
    try:
        logger.info(f"Querying knowledge base with: {query_text}")
        graph_store = get_graph_store()
        vector_store = get_vector_store()
        storage_context = StorageContext.from_defaults(graph_store=graph_store, vector_store=vector_store)

        # Load indices from storage
        # Note: For Simple stores, this just reuses the in-memory instance.
        # For persistent stores (Memgraph, Faiss), this would connect/load.
        kg_index = KnowledgeGraphIndex.from_documents(
            [], # No new documents, load from storage
            storage_context=storage_context,
            # We might need to pass llm/embed_model here if not using global Settings
        )
        # vector_index = VectorStoreIndex.from_documents([], storage_context=storage_context)

        # Create query engine (Graph RAG)
        # We can customize retriever modes, response modes, etc.
        query_engine = kg_index.as_query_engine(
            include_text=True, # Include text from documents in response
            retriever_mode="keyword", # or "embedding" or "hybrid"
            response_mode="tree_summarize", # or "compact"
            # Add specific graph RAG parameters if needed
            # graph_store_query_depth=2,
        )

        response = query_engine.query(query_text)
        logger.info(f"Received response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}", exc_info=True)
        return None


def query_knowledge_base(query_text):
    """
    Recebe um texto de consulta e retorna a resposta do mecanismo de busca baseado em índices.
    """
    setup_llama_index_settings()

    try:
        # Inicializa os armazenamentos (poderia ser persistente no futuro)
        graph_store = get_graph_store()
        vector_store = get_vector_store()
        storage_context = StorageContext.from_defaults(
            graph_store=graph_store,
            vector_store=vector_store
        )

        # Cria índices (em produção isso viria de dados previamente indexados)
        graph_index = KnowledgeGraphIndex.from_documents([], storage_context=storage_context)
        vector_index = VectorStoreIndex.from_documents([], storage_context=storage_context)

        # Cria mecanismos de busca
        graph_engine = graph_index.as_query_engine()
        vector_engine = vector_index.as_query_engine()

        # Executa a consulta nos dois
        graph_response = graph_engine.query(query_text)
        vector_response = vector_engine.query(query_text)

        # Combina ou escolhe uma das respostas
        return f"Graph: {graph_response}\nVector: {vector_response}"

    except Exception as e:
        logger.error(f"Erro ao consultar base de conhecimento: {e}", exc_info=True)
        return "Erro ao processar a consulta na base de conhecimento."
