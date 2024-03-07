import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()

logFileHandler = logging.FileHandler(
    filename="logging.json", mode="w", encoding="utf-8"
)
logStreamHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(pathname)s %(funcName)s",
    json_indent=4,
    json_ensure_ascii=False,
)

logStreamHandler.setFormatter(formatter)
logFileHandler.setFormatter(formatter)
logger.addHandler(logStreamHandler)
logger.addHandler(logFileHandler)
logger.setLevel(settings.LOG_LEVEL)
