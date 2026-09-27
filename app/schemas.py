from pydantic import BaseModel
class ChatRequest(BaseModel):
    document_id:int
    question:str
class ChatResponse(BaseModel):
    answer:str
    document_id:int
    retrieved_chunks:int