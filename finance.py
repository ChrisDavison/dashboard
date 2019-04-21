"""Routes for my purchase history"""
import json
import os
import sqlite3
from pathlib import Path

from flask import render_template, request, Blueprint
from markdown import markdown

BP_FINANCE = Blueprint("finance", __name__, template_folder="templates")
DB_PATH = str((Path(os.environ["DATADIR"]) / "data.db").resolve())


@BP_FINANCE.route("/finance/")
def finances():
    """Return all purchases"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("""select sum(cost) from finances""")
    total = cursor.fetchone()[0]

    cursor.execute("""select distinct category from finances""")
    categories = ", ".join([c[0] for c in cursor.fetchall()])

    cursor.execute(
        """select date, description, category, cost
        FROM finances
        order by date, category, description
    """
    )
    purchases = [
        {"date": date, "description": description, "category": category, "cost": cost}
        for (date, description, category, cost) in cursor.fetchall()
    ]
    start = purchases[0]["date"]
    total_str = markdown(f"**£{total:.0f}** spent on {categories} since *{start}*")
    return render_template("finances.html", finances=purchases, extra_pre=total_str)


@BP_FINANCE.route("/finance/new", methods=["POST"])
def new():
    """Create a new finance purchase, and write to json"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute(
        f"""
        INSERT INTO finances(date, description, category, cost)
        VALUES (
            '{request.form["date"]}',
            '{request.form["description"]}',
            '{request.form["category"]}',
            '{request.form["cost"]}'
        )"""
    )
    db.commit()
    db.close()

    return finances()


@BP_FINANCE.route("/finance/add")
def add():
    """Form to add a new expense/purchase"""
    return render_template("add_expense.html", title="Add a new purchase")
