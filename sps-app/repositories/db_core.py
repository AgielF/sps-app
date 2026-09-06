import pymysql
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

class DatabaseConnection:
    @staticmethod
    def get_connection():
        return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **DB_CONFIG)

    @staticmethod
    def execute_query(sql, params=None):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def execute_fetchone(sql, params=None):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def execute_update(sql, params=None):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
