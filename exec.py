import logging
import pprint
from core import Storage
from core import correios

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    codes = ['JN497032849BR', 'JN497032852BR']

    db = Storage('db.sqlite3')
    for code in codes:
        tracking = correios(code)[-1]
        tracking.update({'code': code})

        row = db.select(('code', "'%s'" % code))
        if row is None:
            db.insert(tracking)
        else:
            if (row.get('mensagem') != tracking['mensagem'])  or (row.get('mensagem') != tracking['mensagem']):
                # TODO mudança de status notify / update item
                print('item mudou o stauts')
                db.update(code, tracking)
            else:
                print('mesmo status')
