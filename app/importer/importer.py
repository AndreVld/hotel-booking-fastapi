import codecs
import csv
import json
from datetime import datetime as dt

from fastapi import UploadFile
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.database import async_session
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.logger import logger

MODELS = {
    "Bookings": Bookings,
    "Hotels": Hotels,
    "Rooms": Rooms,
}


class Importer:

    @classmethod
    def _process_row(cls, row):
        for key, value in row.items():
            if value.isdigit():
                row[key] = int(value)
            elif key.startswith("date"):
                row[key] = dt.strptime(value, "%Y-%m-%d")
            elif key.startswith("services"):
                row[key] = json.loads(value.replace("'", '"'))

        return row

    @classmethod
    def _read_csv(cls, file: UploadFile) -> list[dict]:
        try:
            csv_reader = csv.DictReader(
                codecs.iterdecode(file.file, "utf-8"), delimiter=";"
            )
            data_from_csv = [cls._process_row(row) for row in csv_reader]

            file.file.close()

            logger.info(
                "Retrieved data from CSV file",
                extra={"data": data_from_csv},
            )

            return data_from_csv
        except Exception:
            logger.error("cannot get data from csv file.", exc_info=True)

    @classmethod
    async def insert_data_from_csv(cls, file: UploadFile, table_name: str):
        data = cls._read_csv(file)
        model = MODELS.get(table_name)

        try:
            add_data_to_table = insert(model).values(data)
            async with async_session() as session:
                await session.execute(add_data_to_table)
                await session.commit()
        except SQLAlchemyError:
            logger.error("EXP insert data", exc_info=True)
