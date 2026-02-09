from app.retriever import InMemoryRetriever
from fastapi import FastAPI, UploadFile, File
from app.embeddings import EmbeddingModel
from app.retriever import DocumentProcessor
from app.schemas import IngestResponse
import tempfile
import os
def confidence_label(score: float) -> str:
    if score >= 0.75:
        return "High"
    elif score >= 0.5:
        return "Medium"
    else:
        return "Low"

app = FastAPI(title="Endee-powered RAG API")

retriever = InMemoryRetriever()
embedding_model = EmbeddingModel()
doc_processor = DocumentProcessor()

@app.get("/")
def health_check():
    return {"status": "running", "vector_db": "Endee"}

@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest a PDF document:
    - extract text
    - chunk it
    - generate embeddings
    """
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Load and process document
    text = doc_processor.load_pdf(tmp_path)
    chunks = doc_processor.chunk_text(text)

    # Generate embeddings (not stored yet)
    embeddings = embedding_model.embed_batch(chunks)

    # Cleanup temp file
    os.remove(tmp_path)
    retriever.add(chunks, embeddings)


    return IngestResponse(
        document_name=file.filename,
        chunks_created=len(chunks)
    )

from app.schemas import QuestionRequest, AnswerResponse

@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    question = payload.question

    query_embedding = embedding_model.embed_text(question)
    results = retriever.search(query_embedding, top_k=3)

    # Filter weak matches
    results = [r for r in results if r["score"] >= 0.3]

    if not results:
        return AnswerResponse(
            answer="No sufficiently relevant information found.",
            evidence=[]
        )

    # Add confidence labels
    for r in results:
        r["confidence"] = confidence_label(r["score"])

    # Use top result as concise answer
    answer = results[0]["text"].strip().split("\n")[0]

    return AnswerResponse(
        answer=answer,
        evidence=results
    )

