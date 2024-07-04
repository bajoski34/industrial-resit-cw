import pymysql
from faker import Faker

connection = pymysql.connect(host='localhost',
                            user='bk_store_admin',
                            password='admin',
                            database='bk_store',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

def seed_authors_table(n=100):
    faker = Faker()
    authors = []

    # Generate fake authors
    for _ in range(n):
        first_name = faker.first_name()
        last_name = faker.last_name()
        authors.append((first_name, last_name))

    # Insert into the database
    with connection.cursor() as cursor:
        sql = "INSERT INTO `authors` (`A_FNAME`, `A_LNAME`) VALUES (%s, %s)"
        cursor.executemany(sql, authors)
        connection.commit()

if __name__ == "__main__":
    seed_authors_table()