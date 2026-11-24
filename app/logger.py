
import logging
from pathlib import Path
from datetime import datetime, timedelta


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def setup_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().date()
    log_file = LOG_DIR / f"{today}.log"

    cutoff_date = today - timedelta(days=2)

    for file in LOG_DIR.glob("*.log"):
        try:
            file_date = datetime.strptime(
                file.stem, "%Y-%m-%d"
            ).date()

            if file_date < cutoff_date:
                file.unlink()

        except ValueError:
            continue

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger("etl")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
