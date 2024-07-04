# Expose an API for the Frontend to Consume.
from fastapi import FastAPI
import datetime
import pprint
from pydantic import BaseModel
from .config.services import connection
from .repositories.Library import LibraryRepository
from .repositories.Author import AuthorRepository
from .repositories.Customer import CustomerRepository
app = FastAPI()

bookRepository = LibraryRepository(connection)
authorRepository = AuthorRepository(connection)
customerRepository = CustomerRepository(connection)

class Book(BaseModel):
    title: str | None = None, 
    author_id:int | None = None, 
    publisher:str | None = None, 
    publication_date: datetime.date| None = None, 
    subject: str | None = None, 
    unit_prize: int | None = None,
    stock: int | None = None,

class Customer(BaseModel):
    name: str | None = None,  
    address:str | None = None,

class Author(BaseModel):
    first_name: str | None = None,  
    last_name:str | None = None,

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

@app.post("/books")
async def add(book: Book):
    data = None
    # check if the book exists.
    if bookRepository.ifExists(book.title):
        # If book exists, then update stock. 
        result = bookRepository.find(book.title)
        data = bookRepository.updateInventory(1, 2)
    else:
        # if does not exist create book and then add book to library.
        data = bookRepository.create(book.title, book.author_id, book.publisher, book.publication_date, book.subject, book.unit_prize, 1)

    return {
        "message": "Books Fetched Successfully", 
        "data": data
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

