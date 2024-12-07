import pandas as pd
from typing import *

# TODO: URGENT!!!! PARSE CSV DATA BACK TO AN ARRAY OF USER OBJECTS
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

    #TODO: test
    def remove_row(self, specifier) :
        # Get the index of the specific row using .loc
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
    def make_transaction(self, date, amount, time=None) :
        transaction = Transaction(self, date, amount, time)
        self.transactions.append(transaction)
        return transaction
    
    def create_account(self, balance=0, type='checking') :
        try :
            account = Account(self, balance, type)
            self.accounts.append(account)
        except: 
            print('Couldn\'t create account, make sure your input is valid and try again!')
            self.create_account(self, balance, type)
        return account

    def __str__(self) :
        return f'User ID: {self.id}\n    Username: {self.username}\n    Password: {self.password}'
    
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
    
def start() : 
    answer = str(input('What would you like to do?\n\n1. Login\n2. Register'))
    match answer :
        case '1' :
            login_page()
        case '2' : 
            register_page()
        case _ :
            print("Enter 1 or 2!")
            start()

# UI AND UEx START HERE 

def login_page() :
    username = input('Enter your username: ')
    # While the user doesn't exist, ask the user how they'd like to proceed
    while not username in users.df['username'].values : 
        response = bool_decision('User does not exist, either\n1. Try again\n\nor\n\n2. Register a new  user? ', '1', '2')
        if(response == '1') :
            username = input('Enter your username: ')
        else :
            #TODO: go back to login page after done registering
            register_page()
            exit()
    # get the index of the user in the DataFrame by searching the users DataFrame for the username the user entered.
    user_index = users.df.index[users.df['username'] == username]
    password = input('Enter your password: ')
    # get the correct password by using the .loc DataFrame function to locate the password at a given index.
    correct_password = users.df.loc[user_index, 'password'].tolist()[0]
    while password != correct_password : 
        password = input('Incorrect password, re-enter password')
    print('Correct password entered, continuing to homepage.')
    home_page()

def register_page() : 
    username = input('Enter username: ')
    # if the username already exists, tell them to enter a different one or login
    while username in users.df['username'].values : 
        username = input('User already exists, re-enter username: ')
    password = input('Enter password: ')
    new_user = User(username, password)
    print(f'User created! Info:\n\n{new_user}') 
    
def accounts_page(user) :
    #TODO: prompt user if they want to create an account or add money to an account
    balance = input('Enter the starting balance of this account: ')
    type = input('What type of account will it be? (Checking, Savings, etc.) ')
    new_account = Account(user, balance, type) 
    print(f'Account created! Info:\n\n{new_account}')

def transactions_page(user) :
    amount = input('Enter the amount of the transaction (No dollar sign): ')
    date = input('Enter the date of the transaction (DD/MM/YY): ')
    time_answer = bool_decision('Enter a time? (Y/N): ', 'Y', 'N')
    if time_answer == 'y' :
        time = input('Enter time of transaction (HH:MM:SS):')
    new_transaction = user.make_transaction(amount, date, time)
    print(f'Transaction created! Info:\n\n{new_transaction}')

#TODO: implement and fill out cases
def home_page(user) : 
    print(f'Welcome {user}, what would you like to do?')
    request = input('1. Make a transaction\n2. Open an account\n3. View reports\n4. Help :(')
    match request :
        case '1' :
            transactions_page(user)
        case '2' :
            pass
        case '3' :
            reports_page(user)
        case '4' :
            pass
        case _ :
            pass

#TODO : implement and fill out cases
def reports_page(user) :
    answer = input('What reports would you like to view?\n\n1. Individual Account Summary\n2. Full Accounts Summary\n3. Transaction History')
    match answer : 
        case '1' :
            account = input('Which account would you like to view? ')
            for i in range(0, len(user.accounts)) :
                print(user.accounts[i])
        case '2' : 
            pass
        case '3' :
            pass

# This function exists to validate user input and make sure no invalid decisions are entered.
# It also cleans up my code so I don't have to put a while loop everywhere.
def bool_decision(prompt, option_1, option_2) : 
    option_1 = option_1.lower()
    option_2 = option_2.lower()
    decision = str(input(prompt)).lower()
    while decision != option_1 and decision != option_2 :
        decision = input('Invalid decision, re-enter with proper format: ').lower()
    return decision

print(users.df[0:1])
start()