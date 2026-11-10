from pathlib import Path
from hashlib import sha256
import pymupdf

from climate_ai_management.schemas.document_schema import DocumentHandler
import json
def parse_pdf(file_path:str | Path)->DocumentHandler:
    
    path = Path(file_path)
    
    if not path.is_file():
        raise FileNotFoundError(path)
    
    if path.suffix.lower() != '.pdf':
        raise ValueError("Only pdf docs are allowed!")
    
    pdf_bytes = path.read_bytes()
    
    # Stable identifier for the original document
    document_id = sha256(pdf_bytes).hexdigest()
    pages_data = []
    
    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:
        
        if document.is_encrypted:
            raise ValueError("Encrypted document is not allowed!")
        if document.page_count == 0:
            raise ValueError("Document does not have pages!")
        
      
        for page_num, page in enumerate(document):
            text = page.get_text("text",sort=True)
            layout_doct = page.get_text("dict", sort=True)
            
            pages_data.append({
                "page_number": page_num+1,
                "page_text":text,
                "layout":layout_doct
            })
            
    return DocumentHandler(
        document_id = document_id,
        filename=path.name,
        page_count=len(pages_data),
        page_block=pages_data
    )
    
    
def prepare_pdf_content_for_agent(documentHandler:DocumentHandler)->str:
    
    
    elaborate_page_content = []
    doc_id = documentHandler.document_id
    doc_filename = documentHandler.filename
    
    for pages in documentHandler.page_block:
        page_number = pages.page_number
        page_text = pages.page_text
        
        elaborate_page_content.append({
            
            "Document ID":doc_id,
            "Filename":doc_filename,
            "PageNumber": page_number,
            "Text":page_text
        })
        
    return json.dumps(
        elaborate_page_content,
        ensure_ascii=False,
        indent=2
    )
    
    
def parse_pdf_bytes(pdf_bytes: bytes) -> DocumentHandler:
    document_id = sha256(pdf_bytes).hexdigest()
    pages_data = []

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        if document.needs_pass:
            raise ValueError("Encrypted PDF is not supported")

        for page_num, page in enumerate(document):
            pages_data.append({
                "page_number": page_num + 1,
                "page_text": page.get_text("text", sort=True),
                "layout": page.get_text("dict", sort=True)
            })

    return DocumentHandler(
        document_id=document_id,
        filename="uploaded_document.pdf",
        page_count=len(pages_data),
        page_block=pages_data
    )