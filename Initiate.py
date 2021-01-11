import sys

from DTO import Vaccine, Supplier, Clinic, Logistic
from Repository import repo


def parse_config(path):
    init = False
    with open(path, "r", encoding='utf-8') as file:
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
