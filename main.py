import pandas as pd
import numpy as np

#TODO: see lines 104, 163

class User : 
    def __init__(self, id, username, password, write=True) :
        self.id = id
        self.username = username
        self.password = password
        self.transactions = []
        self.accounts = []
        # write it to the database unless otherwise instructed
        if write :
            users.write_row({'user_id': self.id, 'username': self.username, 'password': password})

    def __str__(self) :
        return self.username
    
class Transaction :
    def __init__(self, id, user, amount, date, time=None, write=True) :
        self.id = id
        self.user = user
        self.amount = amount
        self.date = date
        self.time = time
        self.user.transactions.append(self)
        if write :
            transactions.write_row({'id' : self.id, 'user' : self.user, 'amount' : self.amount, 
            'date' : self.date, 'time' : self.time})

    def __str__(self):
        return f'Transaction #{self.id}: \n    User: {self.user}\n    Amount: {self.amount}\n    Date: {self.date}\n    Time: {self.time}'

class Account : 
    def __init__(self, id, user, balance, type, write=True) :
        self.id = id
        self.user = user
        self.balance = balance
        self.type = type
        self.user.accounts.append(self)
        if write :
            accounts.write_row({'account_id' : self.id, 'user' : self.user, 'balance' : self.balance, 'account_type' : self.type})

    def add_money(self, amount) :
        self.balance += amount

    def __str__(self):
        return f'Account #{self.id}:\n   User: {self.user.username}\n   Balance: {self.balance}\n   Type: {self.type}'

class Database:
    # when a database is created, check to see if it already exists. if it does, read it, if it doesn't, create it
    def __init__(self, filename, columns):
        self.filename = filename
        self.columns = columns
        # attempt to read a stored csv with the requested filename
        try:
            self.df = pd.read_csv(filename).drop(['Unnamed: 0'], axis=1)
        # if it doesn't work, say so and make a new DataFrame for it
        except:
            self.df = pd.DataFrame(columns=columns)
            print('Failed to read csv.')
            # create a new csv with the requested filename since it doesn't exist
            self.df.to_csv(filename, mode='x')
        self.current_index = len(self.df)

    def get_last_index(self):
        return len(self.df)

    # adds a new row to a database instance; payload is a dict with cols and values
    def write_row(self, payload):
        # make sure the length of cols is greater than the length of the data so there's no errors
        cols = list(payload.keys())
        values = list(payload.values())
        index = self.get_last_index()
        for i in range(0, len(cols)):
            self.df.loc[index, str(cols[i])] = values[i]
        self.df.to_csv(self.filename)

        # TODO: test

    def remove_row(self, specifier):
        # Get the index of the specific row using .loc
        index = self.df.loc(self.df[specifier])
        self.df.drop(index)
        self.df.to_csv(self.filename)

    # This method is extremely important. It restores all dead variables back to the program as soon as it is run.
    # Nothing in this program would be possible without this method, and it's made only more convenient by the fact that
    # the index of the object array exactly matches the index of the dataframe, making searching and sorting very easy.
    def parse_objects(self):
        # Get the first letter of the filename to find the type of database (could probably use a dict here)
        arr_type = self.filename[0:1]
        # create a 2d array from the dataframe to more easily get the information
        matrix = self.df.to_numpy()
        print(matrix)
        # loop through the rows and columns of the 2d array, adding the individual values to their own array and then adding 
        # the objects they create to their own array.
        for i in range(0, len(matrix)):
            vals = []
            for j in range(0, len(matrix[i])):
                vals.append(matrix[i][j])
            match arr_type:
                case 'U':
                    new_user = User(vals[0], vals[1], vals[2], False)
                    user_obj_dict[new_user.username] = new_user
                    user_obj_array.append(new_user)
                case 'A':
                    account_obj_array.append(Account(vals[0], user_obj_dict[vals[1]], vals[2], vals[3], False))
                case 'T':
                    transaction_obj_array.append(Transaction(vals[0], user_obj_dict[vals[1]], vals[2], vals[3], vals[4], False))

# Create 3 object arrays and 1 object dict to restore lost variables when program is stopped.
user_obj_dict = {}
user_obj_array = []
account_obj_array = []
transaction_obj_array = []

# Create the three main databases and parse them to the object arrays
users = Database('Users.csv', ['user_id', 'username', 'password'])
users.parse_objects()
accounts = Database('Accounts.csv', ['account_id', 'user', 'balance', 'account_type'])
accounts.parse_objects()
transactions = Database('Transactions.csv', ['transaction_id', 'user', 'amount', 'date', 'time'])
transactions.parse_objects()

# UI AND UEx START HERE

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


def login_page() :
    username = input('Enter your username: ')
    # While the user doesn't exist, ask the user how they'd like to proceed
    while not username in users.df['username'].values : 
        response = bool_decision('User does not exist, either\n1. Try again\n\nor\n\n2. Register a new  user? ', '1', '2')
        if response == '1' :
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
    # TODO: fix this stupid line that doesn't make any sense
    index = np.where(users.df['username'] == username)[0][0]
    # TODO: fix this to actually return the user, not the index or whatever its returning
    home_page(user_obj_array[index])

def register_page() : 
    id = users.get_last_index()
    username = input('Enter username: ')
    # if the username already exists, tell them to enter a different one or login
    while username in users.df['username'].values : 
        username = input('User already exists, re-enter username: ')
    password = input('Enter password: ')
    new_user = User(id, username, password)
    print(f'User created! Info:\n\n{new_user}') 
    
def accounts_page(user) :
    print(user.accounts)
    answer = bool_decision('Would you like to...\n\n1. Create an account\nor\n2. Add money to an existing account?', '1', '2')
    if(answer == '1') :
        id = accounts.get_last_index()
        balance = input('Enter the starting balance of this account: ')
        type = input('What type of account will it be? (Checking, Savings, etc.) ')
        new_account = Account(id, user, balance, type) 
        print(f'Account created! Info:\n\n{new_account}')
    else :
        # Create a dict to prompt the user with a number instead of an account object
        accounts_dict = {}
        print('Which account would you like to add money to?')
        # Loop through the user's account dictionary and add each account to the dict 
        for i in range(0, len(user.accounts)) :
            print(f'{i + 1}. Account #{user.accounts[i].id}')
            accounts_dict[i + 1] = user.accounts[i]
        print(user.accounts)
        account = int(input())
        # If the user doesn't enter a valid number, prompt them to enter a correct one. 
        while account not in accounts_dict.keys():
            account = int(input('Account does not exist, make sure you\'re entering the number provided before the account #!'))
        account_number = accounts_dict[account].id
        amount = float(input(f'How much money would you like to deposit to account #{account_number}? '))
        accounts_dict[account].add_money(amount)   
        print(f'Success! Status of account: \n{accounts_dict[account]}') 

def transactions_page(user) :
    id = transactions.get_last_index()
    amount = input('Enter the amount of the transaction (No dollar sign): ')
    date = input('Enter the date of the transaction (DD/MM/YY): ')
    time_answer = bool_decision('Enter a time? (Y/N): ', 'Y', 'N')
    if time_answer == 'y' :
        time = input('Enter time of transaction (HH:MM:SS):')
    new_transaction = Transaction(id, user, amount, date, time)
    print(f'Transaction created! Info:\n\n{new_transaction}')

#TODO: implement and fill out cases
def home_page(user) : 
    print(f'Welcome {user.username}, what would you like to do?')
    request = input('1. Make a transaction\n2. Open an account\n3. View reports\n4. Help :(')
    match request :
        case '1' :
            transactions_page(user)
        case '2' :
            accounts_page(user)
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

start()