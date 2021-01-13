import sys
from DTO import Vaccine, Supplier, Clinic, Logistic
from Repository import repo


# create new vaccine and updates amount received
def receive_shipment(supplier_name, amount, date):
    vaccine_id = repo.get_next_vaccine_id()  # next available id
    supplier_id, logistic_id = repo.get_supplier_info(supplier_name)
    vaccine = Vaccine(vaccine_id, date, supplier_id, amount)
    repo.vaccines.insert(vaccine)
    repo.update_amount_received(logistic_id, amount)


def send_shipment(location, amount):
    clinic = repo.clinics.find_by_location(location)
    repo.clinics.update_demand(clinic.id, clinic.demand - amount)
    repo.update_amount_sent(clinic.logistic, amount)
    while amount > 0:  # taking amount of vaccines from the inventory
        vaccine = repo.vaccines.find_oldest_vaccine()
        if vaccine.quantity > amount:
            repo.vaccines.update_quantity(vaccine.id, vaccine.quantity - amount)
            amount = 0
        else:
            amount -= vaccine.quantity
            repo.vaccines.remove(vaccine.id)  # quantity of this vaccine is zero


def execute_commands():
    with open(sys.argv[2], "r", encoding='utf-8') as orders, open(sys.argv[3], "w") as output:
        for order_line in orders:
            if order_line[-1] == '\n':  # in case ends with \n remove it
                order_line = order_line[:-1]
            order_params = order_line.split(',')
            if len(order_params) == 3:  # receive shipment order
                receive_shipment(order_params[0], int(order_params[1]), order_params[2])
            elif len(order_params) == 2:  # send shipment order
                send_shipment(order_params[0], int(order_params[1]))
            output.write(repo.get_totals() + '\n')  # log the order executed


def parse_config():
    init = False
    with open(sys.argv[1], "r", encoding='utf-8') as config:
        for line in config:
            if line[-1] == '\n':  # in case ends with \n remove it
                line = line[:-1]
            line_list = line.split(',')
            if not init:  # get number of records for each table
                vaccines_num = int(line_list[0])
                suppliers_num = int(line_list[1])
                clinics_num = int(line_list[2])
                logistics_num = int(line_list[3])
                init = True
            elif vaccines_num > 0:  # insert all the vaccines
                vaccine = Vaccine(*line_list)
                repo.vaccines.insert(vaccine)
                vaccines_num -= 1
            elif suppliers_num > 0:  # insert all the suppliers
                supplier = Supplier(*line_list)
                repo.suppliers.insert(supplier)
                suppliers_num -= 1
            elif clinics_num > 0:  # insert all the clinics
                clinic = Clinic(*line_list)
                repo.clinics.insert(clinic)
                clinics_num -= 1
            elif logistics_num > 0:  # insert all the logistics
                logistic = Logistic(*line_list)
                repo.logistics.insert(logistic)
                logistics_num -= 1


if __name__ == '__main__':
    repo.create_tables()
    parse_config()
    execute_commands()
