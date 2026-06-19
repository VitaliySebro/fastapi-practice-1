import logging
import os
import shutil

from authx import RequestToken
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

# Імпортуємо нашу залежність для перевірки токена
from utils.dependencies import get_current_token

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file to the server",
)
async def upload_file(
    file: UploadFile = File(...),
    token: RequestToken = Depends(
        get_current_token
    ),  # <-- ЗАХИСТ: тепер потрібен JWT-токен
):
    try:
        # Можна дізнатися, який саме користувач завантажує файл

        current_user_id = token.sub

        logger.info(f"User {current_user_id} is uploading file: {file.filename}")

        upload_dir_name = "uploads"

        os.makedirs(upload_dir_name, exist_ok=True)

        file_location = f"{upload_dir_name}/uploaded_{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"info": f"File '{file.filename}' saved at '{file_location}'"}

    except Exception as exc:
        logger.exception("Failed to upload file")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not upload file",
        ) from exc
