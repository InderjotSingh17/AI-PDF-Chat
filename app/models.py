from sqlalchemy import String,ForeignKey,Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from pgvector.sqlalchemy import Vector
class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    file_path:Mapped[str]=mapped_column(String(500))
class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    chunk_text: Mapped[str] = mapped_column(Text)
    embedding= mapped_column(Vector(384))
class ChatMessage(Base):
    __tablename__="chat_messages"
    id:Mapped[int]=mapped_column(primary_key=True)
    document_id:Mapped[int]=mapped_column(ForeignKey("documents.id"))
    role:Mapped[str]=mapped_column(String(20))
    content:Mapped[str]=mapped_column(Text)