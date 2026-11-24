import time
from app.logger import setup_logger
from app.parser import fetch_data
from app.transformer import transform_data
from app.db import Database

def main():
    logger = setup_logger()
    start = "2026-06-01 00:00:00.000000"
    end = "2026-06-02 00:00:00.000000"

    logger.info("ETL started")

    data = fetch_data(start, end)
    logger.info("Data extraction completed: %s records", len(data))

    transformed_data, errors_count = transform_data(data)
    logger.info(
            "Data transformation completed: %s records",
            len(transformed_data)
        )
    if errors_count:
        logger.warning("Rejected records: %s", errors_count)

    db = Database()
    try:
        db.connect()
        logger.info("Database connected")
        db.create_table()
        count_db = db.insert_data(transformed_data)
        logger.info("Data loading completed: %s records", count_db)
    finally:
        db.close()
        logger.info("Connection closed")
    print(f"Получено записей: {len(data)}")
    print(f"Успешно обработано: {len(transformed_data)}")
    print(f"Ошибок трансформации: {errors_count}")
    print(f"Загружено в БД: {count_db}")
if __name__ == "__main__":
    main()