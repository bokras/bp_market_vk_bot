import sqlite3

class DB():
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_chek(self, user_id, price, accaunt_url, market, bill_id):
        with self.connection:
            self.cursor.execute("INSERT INTO 'check' ('user_id', 'price', 'accaunt_url', 'market', 'bill_id') VALUES (?,?,?,?,?)", (user_id,price,accaunt_url,market,bill_id,))

    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'check' WHERE 'bill_id' = ?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]

    def delete_check(self, bill_id):
        with self.connection:
            self.cursor.execute("DELETE FROM 'check' WHERE 'bill_id' = ?", (bill_id,))


    def set_status(self,bill_id,status):
        with self.connection:
            return self.cursor.execute("UPDATE 'check' SET 'status' = ? WHERE 'bill_id' = ?", (status,bill_id,))
