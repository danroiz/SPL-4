from DTO import Supplier, Clinic, Logistic, Vaccine


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def update_quantity(self, vaccine_id, vaccine_quantity):
        c = self._conn.cursor()
        c.execute("""
                UPDATE vaccines
                SET quantity = ({}) WHERE id = ({})
                """.format(vaccine_quantity, vaccine_id))

    def remove(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
                        DELETE FROM vaccines
                        WHERE id = ({})
                        """.format(vaccine_id))

    def get_total_quantity(self):
        c = self._conn.cursor()
        return str(c.execute("""SELECT SUM(quantity) FROM vaccines;""").fetchone()[0])

    def find_oldest_vaccine(self):
        c = self._conn.cursor()
        vaccine = c.execute("""SELECT * FROM vaccines WHERE date = (SELECT MIN(date) FROM vaccines);""").fetchone()
        return Vaccine(*vaccine)

    def get_last_vaccine(self):
        c = self._conn.cursor()
        last_vaccine = c.execute("""
                SELECT * FROM vaccines WHERE ID = (SELECT MAX(ID) FROM vaccines);
                """).fetchone()
        return Vaccine(*last_vaccine)


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.logistic])

    def find_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, logistic FROM suppliers WHERE name = ?
        """, [supplier_name])
        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
               INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
           """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find_by_location(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, demand, logistic FROM clinics WHERE location = ?
        """, [clinic_location])
        return Clinic(*c.fetchone())

    def update_demand(self, clinic_id, clinic_demand):
        c = self._conn.cursor()
        c.execute("""
                UPDATE clinics
                SET demand = ({}) WHERE id = ({})
                """.format(clinic_demand, clinic_id))

    def get_total_demand(self):
        c = self._conn.cursor()
        return str(c.execute("""SELECT SUM(demand) FROM clinics;""").fetchone()[0])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
               INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, count_sent, count_received FROM logistics WHERE id = ?
        """, [logistic_id])
        return Logistic(*c.fetchone())

    def update_count_sent(self, logistic_id, logistic_count_sent):
        c = self._conn.cursor()
        c.execute("""
                UPDATE logistics
                SET count_sent = ({}) WHERE id = ({})
                """.format(logistic_count_sent, logistic_id))

    def update_count_received(self, logistic_id, logistic_count_received):
        c = self._conn.cursor()
        c.execute("""
                UPDATE logistics
                SET count_received = ({}) WHERE id = ({})
                """.format(logistic_count_received, logistic_id))

    def get_total_count_received(self):
        c = self._conn.cursor()
        return str(c.execute("""SELECT SUM(count_received) FROM logistics;""").fetchone()[0])

    def get_total_count_sent(self):
        c = self._conn.cursor()
        return str(c.execute("""SELECT SUM(count_sent) FROM logistics;""").fetchone()[0])

