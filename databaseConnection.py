import mysql.connector

class Database :
    def __init__(self):
        self.db = mysql.connector.connect(
            host='192.168.4.26',
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