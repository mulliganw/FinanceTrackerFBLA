import pandas as pd
from typing import *

class Database :
    # when a database is created, check to see if it already exists. if it does, read it, if it doesn't, create it
    def __init__(self, filename, columns):
        self.filename = filename
        self.columns = columns
        # attempt to read a stored csv with the requested filename
        try: 
            self.df = pd.read_csv(filename).drop(['Unnamed: 0'],axis=1)
        # if it doesn't work, say so and make a new DataFrame for it
        except:
            self.df = pd.DataFrame(columns=columns)
            print('failed to read csv')
            # create a new csv with the requested filename since it doesn't exist
            self.df.to_csv(filename, mode='x')
        self.current_index = len(self.df)
    
    def get_index(self) :
        return len(self.df)
    
    # adds a new row to a database instance
    def write_row(self, data, cols) :
        # make sure the length of cols is greater than the length of the data so there's no errors
        if(len(cols) < len(data)) : 
            return "Excessive data entered; did you make sure there was less data than there was columns?"
        index = self.get_index()
        # TODO: change cols and data to be payload and as a dict
        for i in range(0, len(cols)) :
            self.df.loc[index, str(cols[i])] = data[i]
        self.df.to_csv(self.filename, mode='w')   

    # TODO: implement
    def remove_row() :
        return 0

# Create the three main databases
users = Database('Users.csv', ['user_id', 'username'])
accounts = Database('Accounts.csv', ['account_id', 'user', 'balance', 'account_type'])
transactions = Database('Transactions.csv', ['user', 'amount', 'time'])

class User : 
    def __init__(self, username) :
        self.id = users.get_index()
        self.username = username
        # write all the info to the database
        users.write_row([self.id, self.username], users.columns)  
        self.transactions = []
        self.accounts = []

    # The following two methods are abstracted to the User class so that a user is included by default.
    def make_transaction(self, amount, time=None) :
        transaction = Transaction(self, amount, time)
        self.transactions.append(transaction)
        return transaction
    
    def create_account(self, balance=0, type='checking') :
        account = Account(self, balance, type)
        self.accounts.append(account)
        return account

# TODO: update this to immediately add it to the accounts db
class Transaction :
    def __init__(self, user, amount, time=None) :
        self.id = transactions.get_index()
        self.user = user
        self.amount = amount
        self.time = time
        self.location = location

class Account : 
    # TODO: update this to immediately add it to the accounts db
    def __init__(self, user, balance, type) :
        self.id = accounts.get_index()
        self.user = user
        self.balance = balance
        self.type = type

# TODO: set up test cases with simple terminal input
billy = User('Billy')
