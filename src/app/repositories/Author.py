import pymysql.cursors

class AuthorRepository():
    def __init__(self, connection):
        self.connection = connection

    def ifExists(self, first_name, last_name):
        # TODO: validate title.
        with self.connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM `authors` WHERE `B_FNAME`=%s AND `B_LNAME`=%s LIMIT=1"
            cursor.execute(sql, (first_name, last_name,))
            result = cursor.fetchone()
            return result['COUNT(*)'] > 0

    def create(self, first_name, last_name):
        with self.connection.cursor() as cursor:
            sql = """INSERT INTO `authors` (`A_FNAME`, `A_LNAME`)
                        VALUES (%s, %s)"""
            cursor.execute(sql, (first_name, last_name))
            self.connection.commit()
            return cursor.lastrowid
    
    def find(self, author_id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `author` WHERE `A_ID`=%s LIMIT=1"
            cursor.execute(sql, (author_id,))
            result = cursor.fetchone()
            return result

    def findByName(self, author_name):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `author` WHERE `A_FNAME`=%s LIMIT=1"
            cursor.execute(sql, (author_name,))
            result = cursor.fetchone()
            return result
    
    def list(self):
        # TODO: include pagination. 
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `authors`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def search(self, query):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `Author` WHERE `A_FNAME` LIKE %s OR `A_LNAME` LIKE %s"
            like_query = f"%{query}%"
            cursor.execute(sql, (like_query, like_query,))
            result = cursor.fetchall()
            return result