import pymysql
from faker import Faker
import random

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

def seed_books_table(n=100):
    faker = Faker()
    books = []

    # Fetch author IDs to use in books
    with connection.cursor() as cursor:
        cursor.execute("SELECT `A_ID` FROM `authors`")
        author_ids = [row['A_ID'] for row in cursor.fetchall()]

    # Generate fake books
    for _ in range(n):
        title = faker.sentence(nb_words=5)
        author_id = random.choice(author_ids)
        publisher = faker.company()
        publication_date = faker.date_between(start_date='-10y', end_date='today')
        subject = random.choice(['Fiction', 'Non-Fiction', 'Science', 'Math', 'History'])
        unit_price = round(random.uniform(5.99, 99.99), 2)
        stock = random.randint(1, 50)
        books.append((title, author_id, publisher, publication_date, subject, unit_price, stock))

    # Insert into the database
    with connection.cursor() as cursor:
        sql = """INSERT INTO `books` (`B_TITLE`, `B_A_ID`, `B_PUBLISHER`, `B_PUB_DATE`, `B_SUBJECT`, `B_UNIT_PRIZE`, `B_STOCK`) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(sql, books)
        connection.commit()

def seed_customers_table(n=100):
    faker = Faker()
    customers = []

    # Generate fake customers
    for _ in range(n):
        name = faker.name()
        address = faker.address()
        customers.append((name, address))

    # Insert into the database
    with connection.cursor() as cursor:
        sql = """INSERT INTO `customers` (`C_NAME`, `C_ADD`) 
                 VALUES (%s, %s)"""
        cursor.executemany(sql, customers)
        connection.commit()

def seed_reservations_table(n=100):
    faker = Faker()
    reservations = []

    customers = []
    books = []

    # Fetch customer IDs and book IDs to use in reservations
    with connection.cursor() as cursor:
        cursor.execute("SELECT `C_ID`, `C_NAME` FROM `customers`")
        customers = cursor.fetchall()
        if not customers:
            print("No customers found. Seeding customers table first.")
            seed_customers_table(100)
            cursor.execute("SELECT `C_ID`, `C_NAME` FROM `customers`")
            customers = cursor.fetchall()

        cursor.execute("SELECT `B_ID`, `B_TITLE` FROM `books`")
        books = cursor.fetchall()
        if not books:
            print("No books found. Seeding books table first.")
            seed_books_table(100)
            cursor.execute("SELECT `B_ID`, `B_TITLE` FROM `books`")
            books = cursor.fetchall()

    # Generate fake reservations
    customer_count = len(customers)
    book_count = len(books)
    for i in range(n):
        customer = customers[i % customer_count]
        book = books[i % book_count]
        book_quantity = random.randint(1, 5)
        reservations.append((customer['C_ID'], customer['C_NAME'], book['B_ID'], book['B_TITLE'], book_quantity))

    # Insert into the database
    with connection.cursor() as cursor:
        sql = """INSERT INTO `reservation` (`R_C_ID`, `R_C_NAME`, `R_B_ID`, `R_B_TITLE`, `R_B_QUANTITY`) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.executemany(sql, reservations)
        connection.commit()

if __name__ == "__main__":
    seed_authors_table(50)
    seed_books_table(50)
    seed_customers_table(40)
    seed_reservations_table(30)
