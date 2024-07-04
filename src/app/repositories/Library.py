from uuid import UUID

class LibraryRepository():
    def __init__(self, connection):
        self.connection = connection
    
    def ifExists(self, title):
        # TODO: validate title.
        with self.connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM `books` WHERE `B_TITLE`=%s"
            cursor.execute(sql, (title,))
            result = cursor.fetchone()
            return result['COUNT(*)'] > 0

    
    def create(self, title, author_id, publisher, pub_date, subject, unit_prize, stock):
        with self.connection.cursor() as cursor:
            sql = """INSERT INTO `books` (`B_TITLE`, `B_A_ID`, `B_PUBLISHER`, `B_PUB_DATE`, `B_SUBJECT`, `B_UNIT_PRIZE`, `B_STOCK`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (title, author_id, publisher, pub_date, subject, unit_prize, stock))
            self.connection.commit()
            return cursor.lastrowid
    
    def find(title):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `books` WHERE `B_TITLE`=%s LIMIT=1"
            cursor.execute(sql, (title,))
            result = cursor.fetchone()
            return result
    
    def updateInventory(bookId, new_stock):
        with self.connection.cursor() as cursor:
            sql = "UPDATE `books` SET `B_STOCK`=%s WHERE `B_ID`=%s"
            cursor.execute(sql, (new_stock, bookId))
            self.connection.commit()
            return cursor.lastrowid
    
    def delete(bookId):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM `books` WHERE `B_ID`=%s"
            cursor.execute(sql, (bookId,))
            self.connection.commit()
    
    def list():
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `books`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    
    def edit(bookId, title=None, author_id=None, publisher=None, pub_date=None, subject=None, unit_prize=None, stock=None):
            with self.connection.cursor() as cursor:
                updates = []
                params = []

                if title is not None:
                    updates.append("`B_TITLE`=%s")
                    params.append(title)
                if author_id is not None:
                    updates.append("`B_A_ID`=%s")
                    params.append(author_id)
                if publisher is not None:
                    updates.append("`B_PUBLISHER`=%s")
                    params.append(publisher)
                if pub_date is not None:
                    updates.append("`B_PUB_DATE`=%s")
                    params.append(pub_date)
                if subject is not None:
                    updates.append("`B_SUBJECT`=%s")
                    params.append(subject)
                if unit_prize is not None:
                    updates.append("`B_UNIT_PRIZE`=%s")
                    params.append(unit_prize)
                if stock is not None:
                    updates.append("`B_STOCK`=%s")
                    params.append(stock)

                if not updates:
                    raise ValueError("No fields to update")

                sql = f"UPDATE `books` SET {', '.join(updates)} WHERE `B_ID`=%s"
                params.append(bookId)
                cursor.execute(sql, tuple(params))
                self.connection.commit()
