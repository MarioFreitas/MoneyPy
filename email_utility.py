import email
import imaplib
import getpass
import time
import re
import logging
import sys
import os
from datetime import datetime
from time import sleep
from MoneyPy import *

# GLOBAL VARIABLES
SLEEP_TIME = 10

# Logging Config
logging.basicConfig(filename='./log/log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Username and Password Info
if len(sys.argv) == 3:
    username = sys.argv[1]
    password = sys.argv[2]
    os.system('cls')
else:
    username = input("insert gmail username: ") + "@gmail.com"
    password = getpass.getpass("insert password : ")

# Email login
mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
mail.login(username, password)
mail.select("INBOX")

# Email Verification Loop
def check_email():
   mail.select("INBOX")
   (retcode, messages) = mail.search(None, '(UNSEEN)')
   if retcode == 'OK':
      for num in messages[0].split() :
         typ, data = mail.fetch(num,'(RFC822)')
         for response_part in data:
            if isinstance(response_part, tuple):
                original = email.message_from_bytes(response_part[1])
                if original['Subject'] == "MoneyPy Expense":
                    if original.is_multipart():
                        payload = original.get_payload()[1]
                        add_expense(payload)
                    else:
                        add_expense(original)
                elif original['Subject'] == "MoneyPy Income":
                    if original.is_multipart():
                        payload = original.get_payload()[1]
                        add_income(payload)
                    else:
                        add_income(original)
                elif original['Subject'] == "MoneyPy Gasoline":
                    if original.is_multipart():
                        payload = original.get_payload()[1]
                        add_gasoline(payload)
                    else:
                        add_gasoline(original)
                elif original['Subject'] == "MoneyPy Transfer":
                    if original.is_multipart():
                        payload = original.get_payload()[1]
                        add_transfer(payload)
                    else:
                        add_transfer(original)
                

def add_expense(payload):
    message = payload.get_payload()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    message = message.replace('=', '')
    
    date = message.split("Date:</b> ")[1].split("<br")[0]
    value = message.split("Value:</b> ")[1].split("<br")[0]
    description = message.split("Description:</b> ")[1].split("<br")[0]
    category = message.split("Category:</b> ")[1].split("<br")[0]
    account = message.split("Account:</b> ")[1].split("<br")[0]
    observations = message.split("Observations:</b> ")[1].split("<br")[0]

    date = datetime.strptime(date, '%Y-%m-%d').date()
    value = float(value)
    transaction = Expense(date, value, category, description, account, observations)
    wb = Workbook()
    wb.add_transaction(transaction)
    while True:
        try: 
            wb.save_and_quit()
            break
        except Exception as e:
            print(e)
            logging.error(e)
            sleep(SLEEP_TIME)
            continue
    log_message = f"Expense Added: {date, value, description, category, account, observations}"
    logging.info(log_message)
    print("Expense Added: ", end='')
    print(date, value, description, category, account, observations)

def add_income(payload):
    message = payload.get_payload()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    message = message.replace('=', '')
    
    date = message.split("Date:</b> ")[1].split("<br")[0]
    value = message.split("Value:</b> ")[1].split("<br")[0]
    description = message.split("Description:</b> ")[1].split("<br")[0]
    category = message.split("Category:</b> ")[1].split("<br")[0]
    account = message.split("Account:</b> ")[1].split("<br")[0]
    observations = message.split("Observations:</b> ")[1].split("<br")[0]

    date = datetime.strptime(date, '%Y-%m-%d').date()
    value = float(value)
    transaction = Income(date, value, category, description, account, observations)
    wb = Workbook()
    wb.add_transaction(transaction)
    while True:
        try: 
            wb.save_and_quit()
            break
        except Exception as e:
            print(e)
            logging.error(e)
            sleep(SLEEP_TIME)
            continue
    log_message = f"Income Added: {date, value, description, category, account, observations}"
    logging.info(log_message)
    print("Income Added: ", end='')
    print(date, value, description, category, account, observations)

def add_gasoline(payload):
    message = payload.get_payload()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    message = message.replace('=', '')
    
    date = message.split("Date:</b> ")[1].split("<br")[0]
    value = message.split("Value:</b> ")[1].split("<br")[0]
    category = 'Car Expenses'
    description = 'Gasoline'
    kilometeres = message.split("Kilometers:</b> ")[1].split("<br")[0]
    liters = message.split("Liters:</b> ")[1].split("<br")[0]
    account = message.split("Account:</b> ")[1].split("<br")[0]
    observations = message.split("Observations:</b> ")[1].split("<br")[0]

    date = datetime.strptime(date, '%Y-%m-%d').date()
    value = float(value)
    kilometeres = float(kilometeres)
    liters = float(liters)

    transaction = Expense(date, value, category, description, account, observations)
    wb = Workbook()
    wb.add_transaction(transaction)
    wb.add_gasoline(date, kilometeres, liters)
    while True:
        try: 
            wb.save_and_quit()
            break
        except Exception as e:
            print(e)
            logging.error(e)
            sleep(SLEEP_TIME)
            continue
    log_message = f"Gasoline Added: {date, value, description, category, kilometeres, liters, account, observations}"
    logging.info(log_message)
    print("Gasoline Added: ", end='')
    print(date, value, description, category, kilometeres, liters, account, observations)

def add_transfer(payload):
    message = payload.get_payload()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    message = message.replace('=', '')
    
    date = message.split("Date:</b> ")[1].split("<br")[0]
    value = message.split("Value:</b> ")[1].split("<br")[0]
    category = 'Transfer'
    accountFrom = message.split("Account From:</b> ")[1].split("<br")[0]
    accountTo = message.split("Account To:</b> ")[1].split("<br")[0]
    descriptionFrom = f'To {accountTo}'
    descriptionTo = f'From {accountFrom}'
    observations = message.split("Observations:</b> ")[1].split("<br")[0]

    date = datetime.strptime(date, '%Y-%m-%d').date()
    value = float(value)

    withdraw = Expense(date, value, category, descriptionFrom, accountFrom, observations)
    deposit = Income(date, value, category, descriptionTo, accountTo, observations)
    wb = Workbook()
    wb.add_transaction(withdraw)
    wb.add_transaction(deposit)
    while True:
        try: 
            wb.save_and_quit()
            break
        except Exception as e:
            print(e)
            logging.error(e)
            sleep(SLEEP_TIME)
            continue
    log_message = f"Transfer Added: {date, value, category, accountFrom, accountTo, observations}"
    logging.info(log_message)
    print("Transfer Added: ", end='')
    print(date, value, category, accountFrom, accountTo, observations)

if __name__ == '__main__':
    try:
        check_email()
        print(f"Checked at {datetime.now()}")
        input()
    except Exception as e:
        print(e)
        logging.error(e)
        input()