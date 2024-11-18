import pandas
from typing import *
import mysql.connector
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

class Database :
    def __init__(self):
        self.db = mysql.connector.connect(
            host=f'{IP}',
            user='root',
            password='root',
            port='3306',
            database='financefbla'
        )

    def create_user(self, id, username):
        cursor = self.db.cursor()
        sql = f"""INSERT INTO users(
    id, username)
    VALUES ({id},'{username}')"""
        cursor.execute(sql)
        cursor.execute('SELECT * FROM users')
        print(cursor.fetchall())

    def delete_user(self, id):
        cursor = self.db.cursor()
        cursor.execute(f'DELETE FROM users WHERE id={id}')
        print(cursor.fetchall())
db = Database()
db.create_user(1, 'BillyMulligan')
