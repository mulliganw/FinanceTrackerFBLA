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
    
    # adds a new row to a database instance; payload is a dict with cols and values
    def write_row(self, payload) :
        # make sure the length of cols is greater than the length of the data so there's no errors
        cols = list(payload.keys())
        values = list(payload.values())
        index = self.get_index()
        for i in range(0, len(cols)) :
            self.df.loc[index, str(cols[i])] = values[i]
        self.df.to_csv(self.filename)   

    def remove_row(self, specifier) :
        index = self.df.loc(self.df[specifier])
        self.df.drop(index)
        self.df.to_csv(self.filename)

# Create the three main databases
users = Database('Users.csv', ['user_id', 'username', 'password'])
accounts = Database('Accounts.csv', ['account_id', 'user', 'balance', 'account_type'])
transactions = Database('Transactions.csv', ['user', 'amount', 'date', 'time'])

class User : 
    def __init__(self, username, password) :
        self.id = users.get_index()
        self.username = username
        self.password = password
        # write all the info to the database
        users.write_row({'user_id' : self.id, 'username' : self.username, 'password' : password})  
        # TODO: implement these without the make_transaction or create_account methods, either that or make login
        self.transactions = []
        self.accounts = []

    # The following two methods are abstracted to the User class so that a user is included by default.
    def make_transaction(self, amount, time=None) :
        transaction = Transaction(self, amount, time)
        self.transactions.append(transaction)
        return transaction
    
    def create_account(self, balance=0, type='checking') :
        try :
            account = Account(self, balance, type)
            self.accounts.append(account)
        except: 
            print('Couldn\'t create account, make sure your input is valid!')
        return account

class Transaction :
    def __init__(self, user, amount, date, time=None) :
        self.id = transactions.get_index()
        self.user = user
        self.amount = amount
        self.date = date
        self.time = time
        transactions.write_row({'id' : self.id, 'user' : self.user, 'amount' : self.amount, 
        'date' : self.date, 'time' : self.time})

    def __str__(self):
        return f'Transaction #{self.id}: \n    User: {self.user}\n    Amount: {self.amount}\n    Date: {self.date}\n    Time: {self.time}'

class Account : 
    def __init__(self, user, balance, type) :
        self.id = accounts.get_index()
        self.user = user
        self.balance = balance
        self.type = type
        accounts.write_row({'account_id' : self.id, 'user' : self.user, 'balance' : self.balance, 'account_type' : self.type})

    def __str__(self):
        return f'Account #{self.id}:\n   User: {self.user}\n   Balance: {self.balance}\n    Type: {self.type}'
    
# TODO: comment
def start() : 
    answer = str(input('What would you like to do?\n\n1. Login\n2. Register User\n3. Make an account\n4. Enter a transaction'))
    match answer :
        case '1' :
            username = input('Enter your username: ')
            while not username in users.df['username'].values : 
                username = input('User does not exist, stop program and create a new user instead.')
            user_index = users.df.index[users.df['username'] == username]
            password = input('Enter your password: ')
            while password != users.df.loc[user_index, 'password'].tolist()[0] : 
                password = input('Incorrect password, re-enter password')
            print('Correct password entered, continuing to homepage.')
        case '2' : 
            username = input('Enter username: ')
            while username in users.df['username'].values : 
                username = input('User already exists, re-enter username: ')
            password = input('Enter password: ')
            new_user = User(username, password)
            print(f'User created! Info:\n\n{new_user}')
        case '3' : 
            user = input('Enter the user this account will be used by: ')
            balance = input('Enter the balance of this account: ')
            type = input('What type of account will it be? (Checking, Savings, etc.) ')
            new_account = Account(user, balance, type) 
            print(f'Account created! Info:\n\n{new_account}')
        case '4' :
            user = input('Enter the user this account will be used by: ')
            amount = input('Enter the amount of the transaction (No dollar sign): ')
            date = input('Enter the date of the transaction (DD/MM/YY): ')
            time = input('Enter the time of the transaction (HH:MM:SS): ')
            new_transaction = Transaction(user, amount, date, time)
            print(f'Transaction created! Info:\n\n{new_transaction}')
        case _ :
            print("Enter 1-4!")
            start()

# TODO: implement
def login_page() :
    pass
def register_page() : 
    pass 
def home_page() :
    pass
def accounts_page() :
    pass
def transactions_page(): 
    pass
start()