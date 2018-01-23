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
                if original['Subject'] == "MoneyPy":
                    if original.is_multipart():
                        payload = original.get_payload()[1]
                        add_transaction(payload)
                    else:
                        add_transaction(original)

def add_transaction(payload):
    message = payload.get_payload()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    message = message.replace('=', '')
    split_message = message.split(r'<br />')

    for line in split_message:
        if "Type:" in line:
            pattern = re.compile(r'Type:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            typ = line[end:]
        elif "Date:" in line:
            pattern = re.compile(r'Date:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            date = line[end:]
        elif "Value:" in line:
            pattern = re.compile(r'>Value:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            value = line[end:]
        elif "Description:" in line:
            pattern = re.compile(r'Description:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            description = line[end:]
        elif "Category:" in line:
            pattern = re.compile(r'Category:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            category = line[end:]
        elif "Account:" in line:
            pattern = re.compile(r'Account:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            account = line[end:]
        elif "Observations:" in line:
            pattern = re.compile(r'Observations:</b> ')
            match = list(pattern.finditer(line))[0]
            end = match.span()[1]
            observations = line[end:]
             
    date = datetime.strptime(date, '%Y-%m-%d').date()
    value = float(value)
    if typ == 'Expense':  
        transaction = Expense(date, value, category, description, account, observations)
    elif typ == 'Income': 
        transaction = Income(date, value, category, description, account, observations)
    else:
        raise Exception('Incorrect type')
    wb = Workbook()
    wb.add_transaction(transaction)
    while True:
        try: 
            wb.save_and_quit()
            break
        except Exception as e:
            print(e)
            logging.error(e)
            sleep(60)
            continue
    log_message = f"Transaction Added: {date, value, description, category, account, observations}"
    logging.info(log_message)
    print(log_message)
    # print("Transaction Added: ", end='')
    # print(date, value, description, category, account, observations)


if __name__ == '__main__':
    while True:
        try:
            check_email()
            print(f"Checked at {datetime.now()}")
            sleep(60 * 1)
        except Exception as e:
            print(e)
            logging.error(e)
            continue