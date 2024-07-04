import pymysql.cursors

class ReservationRepository():
    def __init__(self, connection):
        self.connection = connection

    def ifExists(self, customer_id, book_id):
        # TODO: validate title.
        with self.connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM `reservation` WHERE `R_B_ID`=%s AND `R_C_ID`=%s LIMIT=1"
            cursor.execute(sql, (book_id, customer_id,))
            result = cursor.fetchone()
            return result['COUNT(*)'] > 0

    def create(self, customer_id, customer_name, book_id, book_title, book_quantity):
        with self.connection.cursor() as cursor:
            sql = """INSERT INTO `reservation` (`R_C_ID`, `R_C_NAME`, `R_B_ID`, `R_B_TITLE`, `R_B_QUANTITY`)
                        VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (customer_id, customer_name, book_id, book_title, book_quantity))
            self.connection.commit()
            return cursor.lastrowid
    
    def find(self, customer_id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `reservation` WHERE `R_C_ID`=%s LIMIT 1"
            cursor.execute(sql, (author_id,))
            result = cursor.fetchone()
            return result

    def findByCustomerName(self, customer_name):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `reservation` WHERE `R_C_NAME`=%s LIMIT 1"
            cursor.execute(sql, (author_name,))
            result = cursor.fetchone()
            return result
    
    def list(self):
        # TODO: include pagination. 
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `reservation`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def edit(self, reservation_id, customer_id, book_id, quantity):
        with self.connection.cursor() as cursor:
            sql = """
                UPDATE `reservations`
                SET `R_C_ID`=%s, `R_B_ID`=%s, `R_B_QUANTITY`=%s
                WHERE `id`=%s
            """
            cursor.execute(sql, (customer_id, book_id, quantity, reservation_id))
            self.connection.commit()
            return self.findById(reservation_id)

    def delete(self, reservation_id):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM `reservations` WHERE `id`=%s"
            cursor.execute(sql, (reservation_id,))
            self.connection.commit()

    def search(self, query):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `reservation` WHERE `R_ID` LIKE %s OR `R_C_NAME` LIKE %s OR `R_C_ID` LIKE %s"
            like_query = f"%{query}%"
            cursor.execute(sql, (like_query, like_query,))
            result = cursor.fetchall()
            return result