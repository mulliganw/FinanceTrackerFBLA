import pandas
from typing import *

class Transaction :
    total_transactions = 0
    def __init__(self, amount, item, location) : 
        total_transactions += 1
        self.id = total_transactions 
        self.amount = amount
        self.item = item
        self.location = location

class User : 
    total_users = 0 
    def __init__(self, name) :
        total_users += 1
        self.id = total_users
        self.name = name
        self.transactions = []
        self.accounts = []


