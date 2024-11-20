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
        self.df = pd.DataFrame(index=[0], columns=columns)
        try: 
            self.df.to_csv(filename, mode='w')
        except:
            self.df.to_csv(filename, mode='x')
        
    def create_user(self, id, username):
        self.df.loc[self.df.index] = [id, username]
        self.df.index += 1
        self.df.sort_index()
        self.df.to_csv(self.filename, mode='w')
        print(self.df)
    def delete_user(self, id):
        return 0
db = Database('test', ['id', 'username'])
db.create_user(1, 'BillyMulligan')
