import pandas as pd
from typing import *
import socket

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

class Transaction :
    total_transactions = 0
    def __init__(self, amount, item=None, location=None) :
        User.total_transactions += 1
        self.id = User.total_transactions
        self.amount = amount
        self.item = item
        self.location = location

class User : 
    total_users = 0 
    def __init__(self, name) :
        User.total_users += 1
        self.id = User.total_users
        self.name = name
        # Make these two an SQL query later
        self.transactions = []
        self.accounts = []

    def make_transaction(self, amount, item=None, location=None) :
        self.transactions.append(Transaction(amount, item, location))
        
    def create_account(self) :
        self.accounts.append(Account(self.id))

class Account : 
    total_accounts = 0
    def __init__(self, owner, balance=0) :
        Account.total_accounts += 1
        self.id = Account.total_accounts
        self.owner = owner
        self.balance = balance

# TODO: Update __init__ to read the csv and make the dataframe that if it exists already
class Database :
    def __init__(self, filename, columns):
        self.filename = filename
        try: 
            self.df = pd.read_csv(filename, index=False)
        except:
            self.df = pd.DataFrame(columns=columns)
            try: 
                self.df.to_csv(filename, mode='w')
            except:
                self.df.to_csv(filename, mode='x')
        self.current_index = len(self.df.index)

    def create_user(self, username):
        index = len(self.df)
        self.df.loc[index, 'id'] = index + 1
        self.df.loc[index, 'username'] = username
        self.current_index += 1
        self.df.to_csv(self.filename, mode='w')

    def delete_user(self, id):
        self.df.drop(id)
        self.df.sort_index()
        self.df.to_csv(self.filename, mode='w')

db = Database('test.csv', ['id', 'username'])
db.create_user('BillyMulligan')
print(db.df)
