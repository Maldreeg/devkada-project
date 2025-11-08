# Indexing and summarization logic

import faiss
import numpy as np
from typing import List, Dict, Any
import json
import os


class DocumentSummarizer:
    """Handles document indexing and summarization using FAISS"""
    
    def __init__(self, index_path: str = "app/data/indexes", embedding_dim: int = 384):
        """
        Initialize the summarizer
        
        Args:
            index_path: Path to store FAISS index and metadata
            embedding_dim: Dimension of embeddings (default 384 for sentence-transformers)
        """
        self.index_path = index_path
        self.embedding_dim = embedding_dim
        self.index = None
        self.metadata = []
        self.metadata_path = os.path.join(index_path, "metadata.json")
        
        # Create index directory if it doesn't exist
        os.makedirs(index_path, exist_ok=True)
        
        # Load or create index
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create a new one"""
        index_file = os.path.join(self.index_path, "faiss.index")
        
        if os.path.exists(index_file):
            self.index = faiss.read_index(index_file)
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
        else:
            # Create a new index (L2 distance)
            self.index = faiss.IndexFlatL2(self.embedding_dim)
    
    def add_documents(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """
        Add documents to the index
        
        Args:
            embeddings: Document embeddings as numpy array
            metadata: List of metadata dicts for each document
        """
        self.index.add(embeddings)
        self.metadata.extend(metadata)
        self._save_index()
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding as numpy array
            top_k: Number of results to return
            
        Returns:
            List of metadata dicts for top-k similar documents
        """
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['distance'] = float(distances[0][i])
                results.append(result)
        
        return results
    
    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        index_file = os.path.join(self.index_path, "faiss.index")
        faiss.write_index(self.index, index_file)
        
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_document_count(self) -> int:
        """Get the number of indexed documents"""
        return self.index.ntotal if self.index else 0
