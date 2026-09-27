from fastapi import FastAPI,Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Document,DocumentChunk
from app.database import Base, engine
from app import models
from pathlib import Path
from app.services.chunking import chunk_text
from app.services.embeddings import create_embeddings
from app.services.pdf import extract_text
from app.routers.chat import router as chat_router
app = FastAPI()
Base.metadata.create_all(bind=engine)
UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
app.include_router(chat_router)
@app.get("/")
def home():
    return {"message": "AI PDF Chat API is running"}
@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    db:Session=Depends(get_db)
):
    if file.content_type!="application/pdf":
        raise HTTPException(status_code=400,detail="Only PDF files are allowed")
    file_path=UPLOAD_DIR/file.filename
    try:
        with open(file_path,"wb") as buffer:
            contents=await file.read()
            buffer.write(contents)
        document=Document(filename=file.filename,file_path=str(file_path))
        db.add(document)
        db.flush()
        text=extract_text(document.file_path)
        chunks=chunk_text(text)
        embeddings=create_embeddings(chunks)
        for i in range(len(chunks)):
            chunk=DocumentChunk(
                document_id=document.id,
                chunk_text=chunks[i],
                embedding=embeddings[i]
            )
            db.add(chunk)
        db.commit()
        return{
        "message":"PDF uploaded and embeddings stored successfully",
        "filename":document.filename,
        "number_of_chunks":len(chunks),
        "id":document.id
        }
    except Exception as error:
        db.rollback()
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500,detail=str(error))