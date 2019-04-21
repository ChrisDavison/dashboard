"""## Dashboard

- [`/finance/`](/finance/) **or** [and add a new entry](/finance/add)
- [`/books`](/books/) **or** [and add a new entry](/books/add)
- [`/games`](/games/) **or** [and add a new entry](/games/add)
- `/help` - this view
"""
from textwrap import dedent

from flask import Flask, render_template
from markdown import markdown

import finance
import books
import games

APP = Flask(__name__)
APP.register_blueprint(books.BP_BOOKS)
APP.register_blueprint(finance.BP_FINANCE)
APP.register_blueprint(games.BP_GAMES)


@APP.route("/")
@APP.route("/h")
@APP.route("/help")
def help():
    """Display help screen"""
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")
