import logging
import os
from functools import wraps
from typing import Any, Callable, Optional, Self

import psycopg
from psycopg_pool import ConnectionPool

from database.row_factory import DictRowFactory
from dtos.base import BaseDto
from models.user import User


class UsersRepository:

    def __init__(self):
        host = os.environ["POSTGRES_HOST"]
        port = os.environ["POSTGRES_PORT"]
        dbname = os.environ["POSTGRES_DATABASE"]
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        connection_info = f"""
            host={host}
            port={port}
            dbname={dbname}
            user={user}
            password={password}
        """
        psycopg.logger.level = logging.FATAL
        self._connections_pool = ConnectionPool(connection_info, open=True, min_size=10, max_size=100)
        self._cursor: psycopg.Cursor | None = None
        self._setup_tables()

    @staticmethod
    def _with_connection(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(self: Self, *args, **kwargs):
            with self._connections_pool.connection() as connection:
                try:
                    with connection.cursor(row_factory=DictRowFactory) as cursor:
                        self._cursor = cursor
                        result = function(self, *args, **kwargs)
                        self._cursor = None
                except psycopg.errors.IntegrityError:
                    connection.rollback()
                    raise
                except Exception:
                    connection.rollback()
                    raise
                else:
                    connection.commit()
                return result

        return wrapper

    @_with_connection
    def create(self, dto: BaseDto) -> User:
        fields, values = dto.get_fields_values()
        fields_query = str.join(",", fields)
        values_query = str.join(",", ["%s"] * len(values))
        query = f"""
            INSERT INTO users ({fields_query}) VALUES ({values_query}) RETURNING *;
        """
        parameters = values
        response = self._cursor.execute(query.encode(), parameters)
        user_data = response.fetchone()
        if user_data is None:
            raise psycopg.OperationalError
        return User(**user_data)

    @_with_connection
    def read_by_id(self, id: Any) -> Optional[User]:
        query = """
            SELECT * FROM users WHERE id = %s;
        """
        parameters = [id]
        response = self._cursor.execute(query.encode(), parameters)
        user_data = response.fetchone()
        if user_data is None:
            return None
        return User(**user_data)

    @_with_connection
    def read_all(self) -> list[User]:
        pass

    @_with_connection
    def update(self, id: Any, dto: BaseDto) -> Optional[User]:
        pass

    @_with_connection
    def delete(self, id: Any) -> Optional[User]:
        pass

    @_with_connection
    def _setup_tables(self) -> None:
        with open("src/database/postgres_migration.sql", "r") as file:
            self._cursor.execute(file.read().encode())
