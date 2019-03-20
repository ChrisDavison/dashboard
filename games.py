"""Routes for my reading list"""
import json
import os
from flask import request, render_template, Blueprint
from markdown import markdown

BP_GAMES = Blueprint("games", __name__, template_folder="templates")
GAMES_FILE = os.path.join(os.environ["DATADIR"], "games.json")


class Games:
    """games represents a list of games"""

    def __init__(self, filename):
        """Load in the JSON file"""
        self.filename = filename
        self.data = json.load(open(filename, 'r'))
                
    def write(self):
        """If data exists, write it to file"""
        if self.data:
            json.dump(self.data, open(self.filename, "w"), indent=2)
        else:
            print("NO DATA")

    def append(self, item):
        """Append an item to the internal data"""
        self.data.append(item)


@BP_GAMES.route("/games/")
def game_list():
    """Render a list of games, with live filtering"""
    games_list = Games(GAMES_FILE).data
    print(games_list[0])
    platforms = sorted(set(g['Platform'] for g in games_list))
    statuses = sorted(set(g['Status'] for g in games_list if g['Status']))
    platforms_m = f"**Platforms**: {', '.join(platforms)}"
    statuses_m = f"**Status**: {', '.join(statuses)}"
    out = markdown(f"{platforms_m}\n\n{statuses_m}")
    return render_template("games.html", games=games_list, extra_pre=out)


@BP_GAMES.route("/games/new", methods=["POST"])
def new():
    """Add a new game, from the /games/add/ endpoint, to the file"""
    games = Games(GAMES_FILE)
    games.append(
        {
            "Name": request.form["name"],
            "Platform": request.form["platform"],
            "Status": request.form["status"],
            "Multiplayer": request.form["multiplayer"],
            "Comments": request.form["comments"],
            "Released": request.form["released"],
        }
    )
    games.write()
    return render_template(
        "games.html",
        games=games.data[-10:],
        extra_pre=f"Added: {request.form['name']} ({request.form['platform']})",
    )


@BP_GAMES.route("/games/add")
def add():
    return render_template("add_game.html", title="Add a game")
