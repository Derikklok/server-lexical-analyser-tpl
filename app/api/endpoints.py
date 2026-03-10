# app/api/endpoints.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.string_operations import remove_whitespace
from app.utils.tokenizer import tokenize_string

router = APIRouter()

class InputString(BaseModel):
    input_str: str

@router.post("/process_string/")
async def process_string(request: InputString):
    try:
        # Remove whitespaces
        cleaned_str = remove_whitespace(request.input_str)
        
        # Tokenize the cleaned string
        tokens = tokenize_string(cleaned_str)
        
        return {"tokens": tokens}
    
    except Exception as e:
        return {"error": str(e)}