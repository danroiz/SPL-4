from DTO import Vaccine, Supplier, Clinic, Logistic


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM students WHERE id = ?
        """, [vaccine_id])
        return Vaccine(*c.fetchone())

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


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM suppliers WHERE id = ?
        """, [supplier_id])
        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
               INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
           """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM clinics WHERE id = ?
        """, [clinic_id])
        return Clinic(*c.fetchone())

    def update_quantity(self, clinic_id, clinic_demand):
        c = self._conn.cursor()
        c.execute("""
                UPDATE clinics
                SET demand = ({}) WHERE id = ({})
                """.format(clinic_demand, clinic_id))


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
            SELECT id, name FROM clinics WHERE id = ?
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
