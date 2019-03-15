"""Routes for my reading list"""
import json
import os
from flask import request, render_template, Blueprint

BP_LITERATURE = Blueprint("literature", __name__, template_folder="templates")
LITERATURE_FILE = os.path.join(os.environ["DATADIR"], "literature.json")


class Literature:
    """literature represents a list of literature"""

    def __init__(self, filename):
        """Load in the JSON file"""
        self.filename = filename
        self.data = json.load(open(filename))

    def write(self):
        """If data exists, write it to file"""
        if self.data:
            json.dump(self.data, open(self.filename, "w"), indent=2)
        else:
            print("NO DATA")

    def append(self, item):
        """Append an item to the internal data"""
        self.data.append(item)


@BP_LITERATURE.route("/lit/")
def lit_list():
    """Render a list of literature, with live filtering"""
    literature_list = Literature(LITERATURE_FILE).data
    return render_template("literature.html", literature=literature_list)


@BP_LITERATURE.route("/lit/new", methods=["POST"])
def new():
    """Add a new paper, from the /lit/add/ endpoint, to the file"""
    literature = Literature(LITERATURE_FILE)
    ts = [x.strip() for x in request.form["tags"].split(",")]
    auths = [x.strip() for x in request.form["authors"].split(",")]
    synop = [
            request.form["bullet1"],
            request.form["bullet2"],
            request.form["bullet3"],
            request.form["bullet4"],
            request.form["bullet5"],
            ]
    literature.append(
            {
                "Title": request.form["title"],
                "Authors": auths,
                "Year": request.form["year"],
                "Journal": request.form["journal"],
                "Citation": request.form["citation"],
                "Tags": ts,
                "Synopsis": [x for x in synop if x],
                }
            )
    literature.write()
    return render_template(
            "literature.html",
            literature=literature.data,
            extra_pre=f"Added: {request.form['title']}",
            )


@BP_LITERATURE.route("/lit/add")
def add():
    return render_template("add_paper.html", title="Add a book")
