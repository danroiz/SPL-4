import atexit
import sqlite3

from DAO import _Logistics, _Suppliers, _Vaccines, _Clinics


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE logistics (
            id                 INTEGER     PRIMARY KEY,
            name                TEXT       NOT NULL,
            count_sent         INTEGER     NOT NULL,
            count_received     INTEGER     NOT NULL
        );
        
        CREATE TABLE suppliers (
            id                 INTEGER     PRIMARY KEY,
            name                TEXT       NOT NULL,
            logistic           INTEGER    REFERENCES logistics(id)
        );
        
        CREATE TABLE vaccines (
            id      INTEGER     PRIMARY KEY,
            date    DATE        NOT NULL,
            supplier INTEGER    REFERENCES suppliers(id),
            quantity INTEGER NOT NULL 
        );
        
        CREATE TABLE clinics (
            id                 INTEGER     PRIMARY KEY,
            location             TEXT       NOT NULL,
            demand             INTEGER      NOT NULL,
            logistic           INTEGER     REFERENCES logistics(id)
        );
    """)


repo = _Repository()
atexit.register(repo._close)
