from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        # Load the model once (important for performance)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str):
        """
        Convert a single text string into a vector (list of floats)
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]):
        """
        Convert multiple text chunks into vectors
        """
        embeddings = self.model.encode(texts)
        return [vec.tolist() for vec in embeddings]
