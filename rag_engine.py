"""
RAG Engine using LlamaIndex and Groq
"""
from typing import List, Optional
import os

from llama_index.core import (
    VectorStoreIndex,
    Document,
    StorageContext,
    Settings,
    load_index_from_storage,
)
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    EMBEDDING_MODEL,
    VECTOR_STORE_DIR,
)


class RAGEngine:
    """RAG Engine for multimodal document query"""

    def __init__(self):
        self.llm = Groq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY,
            temperature=0.7,
        )
        self.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50

        self.index: Optional[VectorStoreIndex] = None
        self.query_engine = None

        self._load_index()

    def _load_index(self):
        try:
            if os.path.exists(os.path.join(VECTOR_STORE_DIR, "docstore.json")):
                storage_context = StorageContext.from_defaults(
                    persist_dir=VECTOR_STORE_DIR
                )
                self.index = load_index_from_storage(storage_context)
                self.query_engine = self.index.as_query_engine(
                    similarity_top_k=5,
                    response_mode="compact",
                )
        except Exception as e:
            print(f"Could not load existing index: {e}")
            self.index = None

    def add_documents(self, documents: List[Document]):
        if not documents:
            return

        if self.index is None:
            self.index = VectorStoreIndex.from_documents(
                documents,
                show_progress=True,
            )
        else:
            for doc in documents:
                self.index.insert(doc)

        self.index.storage_context.persist(persist_dir=VECTOR_STORE_DIR)

        self.query_engine = self.index.as_query_engine(
            similarity_top_k=5,
            response_mode="compact",
        )

    def query(self, question: str) -> str:
        if self.query_engine is None:
            return "No documents have been indexed yet. Please upload some documents first."
        try:
            response = self.query_engine.query(question)
            return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def get_document_count(self) -> int:
        try:
            if self.index is None:
                return 0
            return len(self.index.docstore.docs)
        except Exception:
            return 0

    def clear_index(self):
        import shutil
        try:
            if os.path.exists(VECTOR_STORE_DIR):
                shutil.rmtree(VECTOR_STORE_DIR)
                os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
            self.index = None
            self.query_engine = None
        except Exception as e:
            print(f"Error clearing index: {e}")
