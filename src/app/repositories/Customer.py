import pymysql.cursors

class CustomerRepository():
    def __init__(self, connection):
        self.connection = connection

    def ifExists(self, name):
        with self.connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM `customers` WHERE `C_NAME`=%s LIMIT 1"
            cursor.execute(sql, (name, address,))
            result = cursor.fetchone()
            return result['COUNT(*)'] > 0

    def create(self, name, address):
        with self.connection.cursor() as cursor:
            sql = """INSERT INTO `customers` (`C_NAME`, `C_ADD`)
                        VALUES (%s, %s)"""
            cursor.execute(sql, (name, address))
            self.connection.commit()
            return cursor.lastrowid
    
    def find(self, customer_id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `customers` WHERE `C_ID`=%s LIMIT 1"
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchone()
            return result

    def findByName(self, customer_name):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `customers` WHERE `C_NAME`=%s LIMIT 1"
            cursor.execute(sql, (customer_name,))
            result = cursor.fetchone()
            return result
    
    def list(self):
        # TODO: include pagination. 
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `customers`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def search(self, query):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `customers` WHERE `C_NAME` LIKE %s OR `C_ADD` LIKE %s"
            like_query = f"%{query}%"
            cursor.execute(sql, (like_query, like_query,))
            result = cursor.fetchall()
            return result