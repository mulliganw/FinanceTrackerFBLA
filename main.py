import pandas
from typing import *

class Transaction :
    total_transactions = 0
    def __init__(self, amount, item, location) : 
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
        self.transactions = []
        self.accounts = []

class Account : 
    total_accounts = 0
    def __init__(self, owner, balance=0) :
        Account.total_accounts += 1
        self.id = Account.total_accounts
        self.owner = owner
        self.balance = balance
