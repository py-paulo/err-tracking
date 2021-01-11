import os
import sqlite3
import logging

from typing import Tuple

logger = logging.getLogger(__name__)

CREATE_TABLE_CORREIOS_SQL = """
create table encomenda (
    id           integer primary key autoincrement not null,
    data         text,
    hora         text,
    local        text,
    mensagem     text,
    code         text
)
"""


class Storage:
    
    def __init__(self, path) -> None:
        if not os.path.exists(path):
            logger.debug('database file does not exist, it will be created')
        self.conn = sqlite3.connect(path)
        
        if not self.conn:
            raise Exception("could not start database")

        try:
            self.init()
        except sqlite3.OperationalError:
            logger.debug('table encomenda already exists')

    def __assert_conn(self):
        pass
    
    def init(self):
        self.conn.executescript(CREATE_TABLE_CORREIOS_SQL)

    def insert(self, document):
        self.conn.executescript("""
        insert into encomenda (data, hora, local, mensagem, code)
        values ('%s', '%s', '%s', '%s', '%s');
        """ % (document['data'], document['hora'], document['local'], document['mensagem'], document['code']))
    
    def update(self, code, document):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM encomenda WHERE code = :code", {'code': code})
        self.insert(document)

    def select(self, key_value: Tuple[str, str] = None):
        cursor = self.conn.cursor()

        cursor.execute("""
        select id, data, hora, local, mensagem, code from encomenda where %s = %s
        """ % (key_value[0], key_value[1]))

        try:
            tracking_id, data, hora, local, mensagem, code = cursor.fetchone()
        except TypeError:
            return None
        else:
            return {
                'id': tracking_id,
                'data': data,
                'hora': hora,
                'local': local,
                'mensagem': mensagem,
                'code': code }

    def select_all(self, filter_by=None):
        cursor = self.conn.cursor()

        cursor.execute("""
        select id, data, hora, local, mensagem from encomenda
        """)

        return [
            {
                'id': tracking_id,
                'data': data,
                'hora': hora,
                'local': local,
                'mensagem': mensagem,
                'code': code
            } for (tracking_id, data, hora, local, mensagem, code) in cursor.fetchall()]

    def save(self):
        pass
    
    def __exit__(self, type, value, traceback):
        self.conn.close()
