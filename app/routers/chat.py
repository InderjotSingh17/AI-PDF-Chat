from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import (
    Document,
    ChatMessage
)
from app.schemas import (
    ChatRequest,
    ChatResponse
)
from app.services.rag import (
    retrieve_relevant_chunks
)
from app.services.llm import (
    generate_answer
)
router = APIRouter()
@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    document = db.get(
        Document,
        request.document_id
    )
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    history_messages = db.execute(
        select(ChatMessage)
        .where(
            ChatMessage.document_id == request.document_id
        )
        .order_by(ChatMessage.id)
        .limit(10)
    ).scalars().all()
    history = ""
    for message in history_messages:
        history += (
            f"{message.role}: "
            f"{message.content}\n"
        )

    chunks = retrieve_relevant_chunks(
        db=db,
        document_id=request.document_id,
        question=request.question,
        top_k=5
    )

    if not chunks:

        raise HTTPException(
            status_code=404,
            detail="No text chunks found for this document"
        )

    context = ""
    for i, chunk in enumerate(chunks):
        context += (
            f"\n--- PDF CHUNK {i + 1} ---\n"
            f"{chunk.chunk_text}\n"
        )

    answer = generate_answer(
        question=request.question,
        context=context,
        history=history
    )

    user_message = ChatMessage(
        document_id=request.document_id,
        role="user",
        content=request.question
    )

    db.add(user_message)

    assistant_message = ChatMessage(
        document_id=request.document_id,
        role="assistant",
        content=answer
    )

    db.add(assistant_message)


    db.commit()

    return ChatResponse(
        answer=answer,
        document_id=request.document_id,
        retrieved_chunks=len(chunks)
    )