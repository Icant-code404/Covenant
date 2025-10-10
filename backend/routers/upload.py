from fastapi import APIRouter, UploadFile, File
from utils.supabase_client import supabase
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

async def upload_contract(file: UploadFile = File(...)):
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}_{file.filename}"

    # Read file bytes
    file_bytes = await file.read()

    # Upload to Supabase Storage (bucket: 'contracts')
    res = supabase.storage.from_("contracts").upload(file_name, file_bytes)
    
    if res:
        return {"status": "success", "file_name": file_name}
    else:
        return {"status": "error", "message": "Upload failed"}
        
