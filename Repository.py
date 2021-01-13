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

    def get_next_vaccine_id(self):
        vaccine = self.vaccines.get_last_vaccine()
        return vaccine.id + 1

    def get_supplier_info(self, name):
        supplier = self.suppliers.find_name(name)
        return supplier.id, supplier.logistic

    def update_amount_received(self, logistic_id, amount):
        logistic = self.logistics.find(logistic_id)
        self.logistics.update_count_received(logistic_id, logistic.count_received+amount)

    def update_amount_sent(self, logistic_id, amount):
        logistic = self.logistics.find(logistic_id)
        self.logistics.update_count_sent(logistic_id, logistic.count_sent+amount)

    def get_totals(self):
        c = self._conn.cursor()
        total_inventory = self.vaccines.get_total_quantity()
        total_demand = self.clinics.get_total_demand()
        total_received = self.logistics.get_total_count_received()
        total_sent = self.logistics.get_total_count_sent()
        return total_inventory + ',' + total_demand + ',' + total_received + ',' + total_sent


repo = _Repository()
atexit.register(repo._close)
