import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

CORREIOS_SQL = """
create table encomenda (
    id           integer primary key autoincrement not null,
    data         text,
    hora         text,
    local        text,
    mensagem     text
)
"""


class Storage:
    
    def __init__(self, path) -> None:
        if not os.path.exists(path):
            logger.debug('database file does not exist, it will be created')
        self.conn = sqlite3.connect(path)
        
        if not self.conn:
            raise Exception("could not start database")
    
    def __assert_conn(self):
        pass
    
    def init(self):
        self.conn.execute(CORREIOS_SQL)

    def insert(self, document):
        cursor = self.conn.cursor()
        
        cursor.execute("insert")

    def save(self):
        pass
    
    def __exit__(self, type, value, traceback):
        self.conn.close()
