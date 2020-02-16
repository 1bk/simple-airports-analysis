import sqlalchemy as db
from sqlalchemy.engine import Connection


class DatabaseConnection:
    """Context Manager for Database Connection using SQL Alchemy."""

    def __init__(self, url):
        try:
            self.pg_engine = db.create_engine(
                name_or_url=url,
                connect_args={'connect_timeout': 10}
            )
            self.connection: Connection = self.pg_engine.connect()
        except Exception as e:
            print('Something went wrong with connection: ', e)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()
