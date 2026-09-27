from sqlalchemy import select
from app.models import DocumentChunk
from app.services.embeddings import model
def retrieve_relevant_chunks(
    db,
    document_id: int,
    question: str,
    top_k: int = 5
):
    """
    Find the PDF chunks that are most relevant to the user's question.
    """
    question_embedding = model.encode(
        question
    ).tolist()
    statement = (
        select(DocumentChunk)
        .where(
            DocumentChunk.document_id == document_id
        )
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                question_embedding
            )
        )
        .limit(top_k)
    )
    results = db.execute(
        statement
    ).scalars().all()
    return results