# Expose an API for the Frontend to Consume.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
import pprint
from pydantic import BaseModel
from .config.services import connection
from .repositories.Library import LibraryRepository
from .repositories.Author import AuthorRepository
from .repositories.Customer import CustomerRepository
from .repositories.Reservation import ReservationRepository
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows
)

bookRepository = LibraryRepository(connection)
authorRepository = AuthorRepository(connection)
customerRepository = CustomerRepository(connection)
reservationRepository = ReservationRepository(connection)
class Book(BaseModel):
    title: str
    author_id:int  
    publisher:str  
    publication_date: datetime.date 
    subject: str
    unit_prize: int
    stock: int 

class Customer(BaseModel):
    name: str 
    address:str

class Author(BaseModel):
    first_name: str
    last_name:str 

class Reservation(BaseModel):
    customer_id: int
    book_id: int
    quantity: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/authors")
async def authors():
    authors = authorRepository.list()
    return {
        "message": "Authors Fetched Successfully", 
        "data": authors
    }

@app.post("/authors")
async def create_author(author: Author):
    author = authorRepository.create(author.first_name, author.last_name)
    return {
        "message": "Authors Created Successfully", 
        "data": author
    }

@app.get("/books")
async def books():
    books = bookRepository.list()
    return {
        "message": "Books Fetched Successfully", 
        "data": books
    }

@app.get("/books/summary")
async def books_summary():
    summary = bookRepository.get_summary()
    return {
        "message": "Books Summary Fetched Successfully",
        "data": summary
    }

@app.post("/books")
async def add(book: Book):
    data = None
    # check if the book exists.
    if bookRepository.ifExists(book.title):
        # If book exists, then update stock. 
        existing_book = bookRepository.findByTitle(book.title)
        bookRepository.updateInventory(existing_book['B_ID'], existing_book['B_STOCK'] + 1)
        data = existing_book['B_ID']
    else:
        # if does not exist create book and then add book to library.
        data = bookRepository.create(book.title, book.author_id, book.publisher, book.publication_date, book.subject, book.unit_prize, 1)

    return {
        "message": "Books Fetched Successfully", 
        "data": {
            "bookId": data
        }
    }

@app.get("/books/{book_id}")
async def get_a_book(book_id: int):
    existing_book = bookRepository.find(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "message": "Book Updated Successfully",
        "data": existing_book
    }

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: Book):
    existing_book = bookRepository.find(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_book = bookRepository.edit(book_id, book.title, book.author_id, book.publisher, book.publication_date, book.subject, book.unit_prize, book.stock)
    return {
        "message": "Book Updated Successfully",
        "data": updated_book
    }

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    existing_book = bookRepository.find(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    bookRepository.delete(book_id)
    return {
        "message": "Book Deleted Successfully"
    }

@app.get("/customers")
async def customers():
    customers = customerRepository.list()
    return {
        "message": "Customers Fetched Successfully", 
        "data": customers
    }

@app.post("/customers")
async def create_customer(customer: Customer):
    customer = customerRepository.create(customer.name, customer.address)
    return {
        "message": "Customer Created Successfully", 
        "data": customer
    }

@app.get("/reservations")
async def reservations():
    reservations = reservationRepository.list()
    return {
        "message": "Customers Fetched Successfully", 
        "data": reservations
    }

@app.post("/reservations")
async def create_reservation(reservation: Reservation):
    # Check if customer exists
    if not customerRepository.find(reservation.customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check if book exists and has enough stock
    book = bookRepository.find(reservation.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book['B_STOCK'] < reservation.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Create reservation
    reservation_id = reservationRepository.create(reservation.customer_id, reservation.book_id, reservation.quantity)
    
    # Update book stock
    bookRepository.updateInventory(reservation.book_id, book['B_STOCK'] - reservation.quantity)

    return {
        "message": "Reservation Created Successfully",
        "data": reservation_id
    }

@app.put("/reservations/{reservation_id}")
async def update_reservation(reservation_id: int, reservation: Reservation):
    existing_reservation = reservationRepository.find(reservation_id)
    if not existing_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    updated_reservation = reservationRepository.edit(reservation_id, reservation.customer_id, reservation.book_id, reservation.quantity)
    return {
        "message": "Reservation Updated Successfully",
        "data": updated_reservation
    }

@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    existing_reservation = reservationRepository.find(reservation_id)
    if not existing_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    reservationRepository.delete(reservation_id)
    return {
        "message": "Reservation Deleted Successfully"
    }
