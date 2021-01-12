import atexit
import sqlite3

from DAO import _Logistics, _Suppliers, _Vaccines, _Clinics
from DTO import Vaccine


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

    def get_next_vaccine_id(self):
        c = self._conn.cursor()
        last_vaccine = c.execute("""
        SELECT * FROM vaccines WHERE ID = (SELECT MAX(ID) FROM vaccines);
        """).fetchone()
        return Vaccine(*last_vaccine).id + 1

    def get_supplier_info(self, name):
        supplier = self.suppliers.find_name(name)
        return supplier.id, supplier.logistic

    def update_amount_received(self, logistic_id, amount):
        logistic = self.logistics.find(logistic_id)
        self.logistics.update_count_received(logistic_id, logistic.count_received+amount)

    def update_amount_sent(self, logistic_id, amount):
        logistic = self.logistics.find(logistic_id)
        self.logistics.update_count_sent(logistic_id, logistic.count_sent+amount)

    def get_oldest_vaccine(self):
        c = self._conn.cursor()
        vaccine = c.execute("""SELECT * FROM vaccines WHERE date = (SELECT MIN(date) FROM vaccines);""").fetchone()
        return Vaccine(*vaccine)

    def get_totals(self):
        c = self._conn.cursor()
        total_inventory = str(c.execute("""SELECT SUM(quantity) FROM vaccines;""").fetchone()[0])
        total_demand = str(c.execute("""SELECT SUM(demand) FROM clinics;""").fetchone()[0])
        total_received = str(c.execute("""SELECT SUM(count_received) FROM logistics;""").fetchone()[0])
        total_sent = str(c.execute("""SELECT SUM(count_sent) FROM logistics;""").fetchone()[0])
        return total_inventory + ',' + total_demand + ',' + total_received + ',' + total_sent


repo = _Repository()
atexit.register(repo._close)
