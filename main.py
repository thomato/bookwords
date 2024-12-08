# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
from pathlib import Path

from processing.processor import process_book

book, stats = process_book(Path("why-we-sleep.epub"))

for key, value in stats.items():
    print(key, value.count)

print(book.title)
print(book.author)
