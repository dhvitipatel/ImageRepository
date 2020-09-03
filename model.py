import sqlite3 as sql

class Schema:
    def get_db_cursor(self):
        conn = sql.connect('inventory.db')
        c = conn.cursor()
        return (c, conn)

    def initialize_db(self):
        (cur, conn)= self.get_db_cursor()
        cur.execute("DROP TABLE IF EXISTS inventory")
        cur.execute('''CREATE TABLE inventory (name TEXT, img TEXT, price INTEGER, qty INTEGER)''')
        cur.execute('''INSERT INTO inventory (name, img, price, qty) VALUES \
            ('Sunflower Feild', 'images/sunflower.jpeg', 18000, 15), \
            ('Fierce Lion', 'images/lion.jpeg', 20000, 20), \
            ('Lemon Aid', 'images/lemon.jpeg', 8000, 30), \
            ('Peacock Feather', 'images/feather.jpeg', 15000, 10), \
            ('Paris Autumn', 'images/paris.jpeg', 12000, 0), \
            ('Mordern Day', 'images/mordern.jpeg', 10000, 15)
        ''')
            
        cur.execute("DROP TABLE IF EXISTS transactions")
        cur.execute("CREATE TABLE transactions (timestamp TEXT, productid INTEGER, value INTEGER)")
        
        # Commit the db changes
        conn.commit()
        print("Initialized database")

    def get_inventory(self):
        (cur,conn) = self.get_db_cursor()
        cur.execute("SELECT rowid, * FROM inventory")
        result = cur.fetchall()
        print("Retrieved %d database entries" % len(result))
        return result

    def get_transactions(self):
        (cur, conn) = Schema().get_db_cursor()
        cur.execute("SELECT SUM(value) FROM transactions")
        result = cur.fetchone()[0]
        return result

    def get_product_info(self, product_id):
        (cur, conn) = Schema().get_db_cursor()
        cur.execute("SELECT rowid, * FROM inventory WHERE rowid = ?", (product_id,))
        result = cur.fetchone()

        if not result: 
            return 'Invalid product ID!'

        if result[4] <= 0:
            return "Insufficient stock!"
        return result


    def do_purchase(self, product_id):
        (cur, conn) = Schema().get_db_cursor()
        cur.execute("SELECT rowid, price, qty FROM inventory WHERE rowid = ?", (product_id,))
        result = cur.fetchone()

        if not result:
            return 'Invalid product ID!'
        (rowid, price, stock) = result

        if stock <= 0:
            return "Insufficient stock!"

        print("Processed transaction of value $%.2f" % (price/100.0))
        cur.execute("INSERT INTO transactions (timestamp, productid, value) VALUES " + \
            "(datetime(), ?, ?)", (rowid, price))

        cur.execute("UPDATE inventory SET qty = qty - 1 WHERE rowid = ?", (product_id,))
        conn.commit()
        return "SUCCESSFUL"

    def add_to_inventory(self, name: str, img: str, price: int, stock: int):
        (cur, conn) = Schema().get_db_cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS inventory (name TEXT, img TEXT, price INTEGER, qty INTEGER)")
        img_path = 'images/'+img
        print(img_path)
        cur.execute('''INSERT INTO inventory (name, img, price, qty) VALUES \
            (?, ?, ?, ?)''', (name, img_path, price, stock))
        conn.commit()
        return "SUCCESSFUL"