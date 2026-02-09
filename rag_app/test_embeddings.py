from app.embeddings import EmbeddingModel

model = EmbeddingModel()

text = "Vector databases are used for semantic search"
vector = model.embed_text(text)

print("Vector length:", len(vector))
print("First 5 values:", vector[:5])
