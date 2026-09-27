def chunk_text(text:str,chunk_size:int=1000):
    chunks=[]
    for start in range(0,len(text),chunk_size):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        return chunks