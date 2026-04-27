from __future__ import annotations

from typing import List, Optional

import pymysql

from memory.memory_item import MemoryItem


class MemoryRepository:
    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.database: str = database

    def _get_connection(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4"
        )

    @staticmethod
    def _row_to_memory_item(row: dict) -> MemoryItem:
        return MemoryItem(
            id=row["id"],
            user_id=row["user_id"],
            key=row["memory_key"],
            value=row["memory_value"],
            type=row["memory_type"],
            importance=row["importance"],
            source=row["source"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def save_or_update(self, memory_item: MemoryItem) -> None:
        sql = """
        INSERT INTO user_memory (
            user_id,
            memory_key,
            memory_value,
            memory_type,
            importance,
            source,
            status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            memory_value = VALUES(memory_value),
            memory_type = VALUES(memory_type),
            importance = VALUES(importance),
            source = VALUES(source),
            status = VALUES(status)
        """

        values = (
            memory_item.user_id,
            memory_item.key,
            memory_item.value,
            memory_item.type,
            memory_item.importance,
            memory_item.source,
            memory_item.status
        )

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def find_by_user_id(self, user_id: int) -> List[MemoryItem]:
        sql = """
        SELECT
            id,
            user_id,
            memory_key,
            memory_value,
            memory_type,
            importance,
            source,
            status,
            created_at,
            updated_at
        FROM user_memory
        WHERE user_id = %s
          AND status = 'active'
        ORDER BY importance DESC, updated_at DESC
        """

        conn = self._get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            return [self._row_to_memory_item(row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    def search_relevant(self, user_id: int, query: str, limit: int = 10) -> List[MemoryItem]:
        sql = """
        SELECT
            id,
            user_id,
            memory_key,
            memory_value,
            memory_type,
            importance,
            source,
            status,
            created_at,
            updated_at
        FROM user_memory
        WHERE user_id = %s
          AND status = 'active'
          AND (
              memory_key LIKE CONCAT('%%', %s, '%%')
              OR memory_value LIKE CONCAT('%%', %s, '%%')
          )
        ORDER BY importance DESC, updated_at DESC
        LIMIT %s
        """

        conn = self._get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, (user_id, query, query, limit))#TODO 111 这里看不懂
            rows = cursor.fetchall()
            return [self._row_to_memory_item(row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    def delete(self, user_id: int, key: str) -> None:
        sql = """
        UPDATE user_memory
        SET status = 'deleted'
        WHERE user_id = %s
          AND memory_key = %s
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (user_id, key))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def find_by_user_id_and_key(self, user_id: int, key: str) -> Optional[MemoryItem]:
        sql = """
        SELECT
            id,
            user_id,
            memory_key,
            memory_value,
            memory_type,
            importance,
            source,
            status,
            created_at,
            updated_at
        FROM user_memory
        WHERE user_id = %s
          AND memory_key = %s
          AND status = 'active'
        LIMIT 1
        """

        conn = self._get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, (user_id, key))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_memory_item(row)
        finally:
            cursor.close()
            conn.close()
