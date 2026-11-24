import logging

import psycopg2
from psycopg2.extras import execute_values

from config.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

logger = logging.getLogger("etl")

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("Database connection established")
    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed")
    def create_table(self):
        cur = self.conn.cursor()
        try:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id BIGSERIAL PRIMARY KEY,
                user_id TEXT NOT NULL,
                oauth_consumer_key TEXT,
                lis_result_sourcedid TEXT,
                lis_outcome_service_url TEXT,
                is_correct BOOLEAN,
                attempt_type TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,

                CHECK (attempt_type IN ('run', 'submit')),
                CHECK (
                    (attempt_type = 'run' AND is_correct IS NULL)
                    OR
                    (attempt_type = 'submit' AND is_correct IS NOT NULL)
                )
            );
            """)
            self.conn.commit()
            logger.info("Table attempts is ready")
        except psycopg2.Error:
            self.conn.rollback()
            logger.exception("Database operation failed")
            raise
        finally:
            cur.close()

    def insert_data(self, data):
        if not data:
            return 0
        cur = self.conn.cursor()
        query = """
        INSERT INTO attempts (
            user_id,
            oauth_consumer_key,
            lis_result_sourcedid,
            lis_outcome_service_url,
            is_correct,
            attempt_type,
            created_at
        ) VALUES %s;
        """
        values = []
        
        try:
            for item in data:
                values.append((
                    item["user_id"],
                    item["oauth_consumer_key"],
                    item["lis_result_sourcedid"],
                    item["lis_outcome_service_url"],
                    item["is_correct"],
                    item["attempt_type"],
                    item["created_at"]
                ))
            execute_values(cur, query, values)
            self.conn.commit()
        except psycopg2.Error:
            self.conn.rollback()
            raise
        finally:
            cur.close()

        return len(data)
        
