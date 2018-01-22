from MoneyPy import *

from datetime import date
date = date(2018, 1, 10)
# e = Expense(date, 200, 'Supermarket', 'Bananas', 'Credit Card')
i = Income(date, 1000, 'Money', 'Smugling', 'Checking Account')
wb = Workbook()
wb.add_transaction(i)
wb.save_and_quit()
# wb.update_summary('Credit Card', 10)
