from pypdf import PdfReader

class DocumentProcessor:
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def load_pdf(self, file_path: str) -> str:
        """
        Load text from a PDF file
        """
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    def chunk_text(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.overlap

        return chunks
import numpy as np

class InMemoryRetriever:
    def __init__(self):
        self.chunks = []
        self.embeddings = []

    def add(self, chunks, embeddings):
        self.chunks.extend(chunks)
        self.embeddings.extend(embeddings)

    def search(self, query_embedding, top_k=3):
        query = np.array(query_embedding)
        scores = []

        for emb in self.embeddings:
            emb = np.array(emb)
            similarity = np.dot(query, emb) / (
                np.linalg.norm(query) * np.linalg.norm(emb)
            )
            scores.append(similarity)

        top_indices = np.argsort(scores)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                "text": self.chunks[idx],
                "score": float(scores[idx])
            })

        return results
import numpy as np

class InMemoryRetriever:
    def __init__(self):
        self.chunks = []
        self.embeddings = []

    def add(self, chunks, embeddings):
        self.chunks.extend(chunks)
        self.embeddings.extend(embeddings)

    def search(self, query_embedding, top_k=3):
        query = np.array(query_embedding)
        scores = []

        for emb in self.embeddings:
            emb = np.array(emb)
            similarity = np.dot(query, emb) / (
                np.linalg.norm(query) * np.linalg.norm(emb)
            )
            scores.append(similarity)

        top_indices = np.argsort(scores)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                "text": self.chunks[idx],
                "score": float(scores[idx])
            })

        return results
