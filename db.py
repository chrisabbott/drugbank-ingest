import logging
import psycopg2


class DrugBankDB(object):
    # CREATE_TABLE and INSERT logic should be offloaded to this class
    def __init__(self, DB_NAME="drugbank-postgres", DB_USER="postgres", DB_PASS="postgres", DB_PORT=5432):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host='localhost', password=DB_PASS)
        self._cursor = None

    @property
    def cursor(self):
        if not self._cursor:
            self._cursor = self.conn.cursor()
        return self._cursor
