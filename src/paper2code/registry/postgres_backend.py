"""PostgreSQL-backed registry implementation using psycopg."""

from __future__ import annotations

import importlib

from paper2code.models import ToolRecord
from paper2code.registry.db_config import get_database_url
from paper2code.registry.tool_registry import ToolRegistryProtocol


class PostgreSQLToolRegistry(ToolRegistryProtocol):
    """Stores tool records in PostgreSQL with a minimal SQL backend."""

    def __init__(self, database_url: str | None = None) -> None:
        """Initialize registry with a PostgreSQL connection URL."""
        self._database_url = database_url or get_database_url()

    def _connect(self):
        """Open a new database connection using psycopg."""
        psycopg = importlib.import_module("psycopg")
        return psycopg.connect(self._database_url)

    def ensure_schema(self) -> None:
        """Create registry table if not already present."""
        create_sql = (
            "CREATE TABLE IF NOT EXISTS tool_records ("
            "tool_id VARCHAR(80) PRIMARY KEY, "
            "name VARCHAR(120) NOT NULL, "
            "modality VARCHAR(80) NOT NULL, "
            "input_contract VARCHAR(500) NOT NULL, "
            "output_contract VARCHAR(500) NOT NULL, "
            "confidence DOUBLE PRECISION NOT NULL"
            ");"
        )
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_sql)
            conn.commit()

    def add_tool(self, record: ToolRecord) -> None:
        """Insert or update one tool record in PostgreSQL."""
        self.ensure_schema()
        sql = (
            "INSERT INTO tool_records "
            "(tool_id, name, modality, input_contract, output_contract, "
            "confidence) VALUES (%s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (tool_id) DO UPDATE SET "
            "name = EXCLUDED.name, "
            "modality = EXCLUDED.modality, "
            "input_contract = EXCLUDED.input_contract, "
            "output_contract = EXCLUDED.output_contract, "
            "confidence = EXCLUDED.confidence"
        )
        params = (
            record.tool_id,
            record.name,
            record.modality,
            record.input_contract,
            record.output_contract,
            record.confidence,
        )
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()

    def list_tools(self) -> list[ToolRecord]:
        """Return all known tool records from PostgreSQL."""
        self.ensure_schema()
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT tool_id, name, modality, input_contract, "
                    "output_contract, confidence "
                    "FROM tool_records ORDER BY tool_id"
                )
                rows = cursor.fetchall()
        return [
            ToolRecord(
                tool_id=row[0],
                name=row[1],
                modality=row[2],
                input_contract=row[3],
                output_contract=row[4],
                confidence=row[5],
            )
            for row in rows
        ]
