from pathlib import Path

from loguru import logger

HERE = Path(__file__).parent.resolve()


def setup_logger(log_file_path=f"{HERE}/../resources/chatbot.log"):
    logger.add(log_file_path, rotation="10 MB", retention="7 days", level="INFO")
