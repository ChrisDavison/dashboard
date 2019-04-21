"""Routes for my reading list"""
import json
import os
import sqlite3
from pathlib import Path

from flask import request, render_template, Blueprint


BP_BOOKS = Blueprint("books", __name__, template_folder="templates")
BOOKS_FILE = os.path.join(os.environ["DATADIR"], "reading-list.json")
DB_PATH = str((Path(os.environ["DATADIR"]) / "data.db").resolve())


@BP_BOOKS.route("/books/")
def book_list():
    """Render a list of books, with live filtering"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("""select distinct genre from reading order by genre""")
    genres = cursor.fetchall()
    out = []
    for genre in genres:
        cursor.execute(f"""
            select * from reading
            where genre='{genre[0]}'
            order by title""")
        data = cursor.fetchall()
        if data:
            out.extend([{
                'Title': title,
                'Author': author,
                'Genre': genre,
                'Status': status,
                'Read': read}
                for (_, title, author, genre, status, read) in data
            ])
    db.close()
    return render_template("books.html", books=out)


@BP_BOOKS.route("/books/new", methods=["POST"])
def new():
    """Add a new book, from the /books/add/ endpoint, to the file"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute(f"""
        INSERT INTO reading(title, author, genre, status, read)
        VALUES (
            '{request.form["title"]}',
            '{request.form["author"]}',
            '{request.form["genre"]}',
            '{request.form["status"]}',
            '{request.form["read"]}'
        )""")
    db.commit()
    db.close()

    return book_list()


@BP_BOOKS.route("/books/add")
def add():
    return render_template("add_book.html", title="Add a book")
