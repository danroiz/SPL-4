# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Repository import repo
import Initiate
import sys
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if not os.path.isfile('database.db'):
        repo.create_tables()
        Initiate.parse_config(sys.argv[1])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
