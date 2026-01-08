"""
RAG Engine using LlamaIndex and Groq
"""
from typing import List, Optional
from llama_index.core import (
    VectorStoreIndex,
    Document,
    StorageContext,
    Settings,
)
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from config import GROQ_API_KEY, GROQ_MODEL, EMBEDDING_MODEL, VECTOR_STORE_DIR, COLLECTION_NAME


class RAGEngine:
    """RAG Engine for multimodal document query"""
    
    def __init__(self):
        """Initialize the RAG engine with Groq LLM and embeddings"""
        
        # Initialize Groq LLM
        self.llm = Groq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY,
            temperature=0.7,
        )
        
        # Initialize embeddings
        self.embed_model = HuggingFaceEmbedding(
            model_name=EMBEDDING_MODEL
        )
        
        # Set global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        
        # Initialize Chroma vector store
        self.chroma_client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
        self.chroma_collection = self.chroma_client.get_or_create_collection(COLLECTION_NAME)
        
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        
        # Index
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine = None
        
        # Try to load existing index
        self._load_index()
    
    def _load_index(self):
        """Load existing index if available"""
        try:
            # Check if collection has documents
            if self.chroma_collection.count() > 0:
                self.index = VectorStoreIndex.from_vector_store(
                    self.vector_store,
                    storage_context=self.storage_context
                )
                self.query_engine = self.index.as_query_engine(
                    similarity_top_k=5,
                    response_mode="compact"
                )
        except Exception as e:
            print(f"Could not load existing index: {e}")
            self.index = None
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to the index
        
        Args:
            documents: List of LlamaIndex Document objects
        """
        if not documents:
            return
        
        if self.index is None:
            # Create new index
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context,
                show_progress=True
            )
        else:
            # Add to existing index
            for doc in documents:
                self.index.insert(doc)
        
        # Update query engine
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=5,
            response_mode="compact"
        )
    
    def query(self, question: str) -> str:
        """
        Query the RAG system
        
        Args:
            question: User question
            
        Returns:
            Answer from the RAG system
        """
        if self.query_engine is None:
            return "No documents have been indexed yet. Please upload some documents first."
        
        try:
            response = self.query_engine.query(question)
            return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def get_document_count(self) -> int:
        """Get the number of documents in the index"""
        try:
            return self.chroma_collection.count()
        except:
            return 0
    
    def clear_index(self):
        """Clear all documents from the index"""
        try:
            self.chroma_client.delete_collection(COLLECTION_NAME)
            self.chroma_collection = self.chroma_client.get_or_create_collection(COLLECTION_NAME)
            self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            self.index = None
            self.query_engine = None
        except Exception as e:
            print(f"Error clearing index: {e}")
