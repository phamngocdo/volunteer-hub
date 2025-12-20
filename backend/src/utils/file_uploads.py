import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile

def save_image(file: UploadFile, folder: str) -> str:
    upload_dir = Path(f"frontend/public/{folder}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = upload_dir / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"public/{folder}/{filename}"
