import pandas as pd
from typing import *

class Database :
    def __init__(self, filename, columns):
        self.filename = filename
        self.columns = columns
        try: 
            self.df = pd.read_csv(filename).drop(['Unnamed: 0'],axis=1)
        except:
            self.df = pd.DataFrame(columns=columns)
            print('failed to read csv')
            try: 
                self.df.to_csv(filename, mode='w')
            except:
                self.df.to_csv(filename, mode='x')
        self.current_index = len(self.df)
    
    def get_index(self) :
        return len(self.df)
    
    def write_row(self, data, cols) :
        if(len(cols) < len(data)) : 
            return "Excessive data entered; did you make sure there was less data than there was columns?"
        index = len(self.df)
        for i in range(0, len(cols)) :
            self.df.loc[index, str(cols[i])] = data[i]
        self.current_index += 1
        self.df.to_csv(self.filename, mode='w')   

    def remove_row() :
        return 0

    def delete_user(self, id):
        self.df.drop(id)
        self.df.sort_index()
        self.df.to_csv(self.filename, mode='w')

# Create the three main databases
# TODO: Move database class above everything else and define these beforehand so I don't have to take in 
# db as a param
users = Database('Users.csv', ['user_id', 'username'])
accounts = Database('Accounts.csv', ['account_id', 'user', 'balance', 'account_type'])
transactions = Database('Transactions.csv', ['user', 'amount', 'location', 'time'])

class Transaction :
    total_transactions = 0
    def __init__(self, user, amount, location=None, time=None) :
        self.id = transactions.get_index()
        self.user = user
        self.amount = amount
        self.time = time
        self.location = location

class User : 
    def __init__(self, username) :
        self.id = users.get_index()
        self.username = username
        users.write_row([self.id, self.username], users.columns)  
        # These should be their own dataframes in the future.     
        self.transactions = []
        self.accounts = []

    def make_transaction(self, amount, item=None, location=None) :
        self.transactions.append(Transaction(amount, item, location))
        
    def create_account(self) :
        self.accounts.append(Account(self.id))

class Account : 
    def __init__(self, user, balance=0, type='checking') :
        self.id = accounts.get_index()
        self.user = user
        self.balance = balance
        self.type = type

billy = User('Billy', users)
