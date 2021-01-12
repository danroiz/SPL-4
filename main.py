from DTO import Vaccine, Supplier, Clinic, Logistic
from Repository import repo
import sys


def summary_add(log_line):
    with open('output.txt', 'a') as out:
        out.write(log_line + '\n')


def receive_shipment(supplier_name, amount, date):
    vaccine_id = repo.get_next_vaccine_id()
    supplier_id, logistic_id = repo.get_supplier_info(supplier_name)
    vaccine = Vaccine(vaccine_id, date, supplier_id, amount)
    repo.vaccines.insert(vaccine)
    repo.update_amount_received(logistic_id, amount)


def send_shipment(location, amount):
    clinic = repo.clinics.find_by_location(location)
    repo.clinics.update_demand(clinic.id, clinic.demand - amount)
    repo.update_amount_sent(clinic.logistic, amount)
    while amount > 0:
        vaccine = repo.get_oldest_vaccine()
        if vaccine.quantity > amount:
            repo.vaccines.update_quantity(vaccine.id, vaccine.quantity - amount)
            amount = 0
        else:
            amount -= vaccine.quantity
            repo.vaccines.remove(vaccine.id)


def execute_commands():
    with open('orders.txt', "r", encoding='utf-8') as file:
        for line in file:
            if line[-1] == '\n':
                line = line[:-1]
            line_list = line.split(',')
            if len(line_list) == 3:
                receive_shipment(line_list[0], int(line_list[1]), line_list[2])
            elif len(line_list) == 2:
                send_shipment(line_list[0], int(line_list[1]))
            summary_add(repo.get_totals())


def parse_config():
    init = False
    with open('config.txt', "r", encoding='utf-8') as file:
        for line in file:
            if line[-1] == '\n':
                line = line[:-1]
            line_list = line.split(',')
            print(line_list)
            if not init:
                print(line_list[0])
                vaccines_num = int(line_list[0])
                suppliers_num = int(line_list[1])
                clinics_num = int(line_list[2])
                logistics_num = int(line_list[3])
                init = True
            elif vaccines_num > 0:
                vaccine = Vaccine(*line_list)
                repo.vaccines.insert(vaccine)
                vaccines_num -= 1
            elif suppliers_num > 0:
                supplier = Supplier(*line_list)
                repo.suppliers.insert(supplier)
                suppliers_num -= 1
            elif clinics_num > 0:
                clinic = Clinic(*line_list)
                repo.clinics.insert(clinic)
                clinics_num -= 1
            elif logistics_num > 0:
                logistic = Logistic(*line_list)
                repo.logistics.insert(logistic)
                logistics_num -= 1


if __name__ == '__main__':
    repo.create_tables()
    parse_config()  # sys.argv[1])
    execute_commands()

