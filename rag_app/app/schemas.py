from pydantic import BaseModel
from typing import List

class IngestResponse(BaseModel):
    document_name: str
    chunks_created: int
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    evidence: list

