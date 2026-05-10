import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .pdf_processor import extract_text_from_pdf

class RAGManager:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            # Using a lightweight model for efficiency
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._model

    @staticmethod
    def chunk_text(text, chunk_size=500, overlap=50):
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])
        return chunks

    @classmethod
    def create_index(cls, text):
        chunks = cls.chunk_text(text)
        if not chunks:
            return None, []
        
        model = cls.get_model()
        embeddings = model.encode(chunks)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        return index, chunks

    @classmethod
    def query_index(cls, index, chunks, query, k=3):
        if not index or not chunks:
            return ""
        
        model = cls.get_model()
        query_embedding = model.encode([query])
        
        D, I = index.search(np.array(query_embedding).astype('float32'), k)
        
        results = [chunks[i] for i in I[0] if i < len(chunks)]
        return " ".join(results)
