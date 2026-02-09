from app.retriever import DocumentProcessor

processor = DocumentProcessor()

text = """
Vector databases store embeddings for similarity search.
They are widely used in semantic search and RAG systems.
Endee is a high-performance vector database.
"""

chunks = processor.chunk_text(text)

print("Number of chunks:", len(chunks))
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}:\n{chunk}")
