from enum import Enum

from fastapi import APIRouter, File, Path, UploadFile

from app.importer.importer import Importer
from app.logger import logger

router = APIRouter(
    prefix="/import",
    tags=["Importer"],
)


class ModelName(str, Enum):
    Hotels = "Hotels"
    Rooms = "Rooms"
    Bookings = "Bookings"


@router.post("/{model_name}")
async def import_from_csv(model_name: ModelName = Path(), file: UploadFile = File()):
    logger.info(
        f"Import from {file.filename} to table {model_name}",
        extra={"file_name": file.filename, "model_name": model_name},
    )
    await Importer.insert_data_from_csv(file=file, table_name=model_name.value)
