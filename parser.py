from pathlib import Path
import fitz 
from docx import Document

def parse_document(file_path: str) -> dict:
   
    path = Path(file_path)
    file_name = path.name
    extension = path.suffix.lower()
    
    text = ""
    num_pages = 0

    if extension == ".pdf":
        with fitz.open(file_path) as doc:
            num_pages = len(doc)
            for page in doc:
                text += page.get_text()
                
    elif extension in [".docx", ".doc"]:
        doc = Document(file_path)
        
        text = "\n".join([para.text for para in doc.paragraphs])
       
        num_pages = 0 
        
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    text = text.strip()

    return {
        "file_name": file_name,
        "num_pages": num_pages,
        "text": text
    }


