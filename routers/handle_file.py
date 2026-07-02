import shutil
from fastapi import UploadFile
from fastapi import APIRouter, File

router = APIRouter(tags=["Handle File"], prefix="/file")


@router.post("/")
def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    content_line = content.split("\n")
    return {"content": content_line}

@router.post("/upload")
def upload_file(upload_file:UploadFile= File(...)):
    path = f"uploaded_files/{upload_file.filename}"
    with open(path,"w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {"file_name": upload_file.filename}