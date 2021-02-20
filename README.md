# SPL-4
Python and SQL

# In this project we will implement a database of a SARS-CoV-2 vaccine distribution center.

The project is composed of three parts:

1. Create and populate the database according to a configuration file.
2. Execute a list of orders, according to a second file.
3. Print a summary in a third file.

# To run the project use:

python3 main . py c o n f i g . t x t o r d e r s . t x t output . t x t

# To run the automated test use:

python3 compare_output.py true_output.txt tested_output.txt db_true.db db_tested.db