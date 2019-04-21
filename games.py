"""Routes for my reading list"""
import json
import os
import sqlite3
from pathlib import Path
from flask import request, render_template, Blueprint
from markdown import markdown

BP_GAMES = Blueprint("games", __name__, template_folder="templates")
DB_PATH = str((Path(os.environ["DATADIR"]) / "data.db").resolve())


@BP_GAMES.route("/games/")
def game_list():
    """Render a list of games, with live filtering"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT name, platform, status, multiplayer, comments, released FROM gaming ORDER BY platform, name"""
    )
    fetched = cursor.fetchall()
    data = [
        {
            "Name": name,
            "Platform": platform,
            "Status": status,
            "Multiplayer": multiplayer,
            "Comments": comments,
            "Released": released,
        }
        for name, platform, status, multiplayer, comments, released in fetched
    ]

    cursor.execute(
        f"""
        SELECT distinct platform from gaming order by platform"""
    )
    platforms = [c[0] for c in cursor.fetchall()]

    cursor.execute(
        f"""
        SELECT distinct status from gaming
        WHERE status is not null
        order by status"""
    )
    statuses = [c[0] for c in cursor.fetchall()]

    platforms_m = f"**Platforms**: {', '.join(platforms)}"
    statuses_m = f"**Status**: {', '.join(statuses)}"
    out = markdown(f"{platforms_m}\n\n{statuses_m}")
    return render_template("games.html", games=data, extra_pre=out)


@BP_GAMES.route("/games/new", methods=["POST"])
def new():
    """Add a new game, from the /games/add/ endpoint, to the file"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute(
        f"""
        INSERT INTO gaming(
            name, platform, status, multiplayer, comments, released
        )
        VALUES (
            '{request.form["name"]}',
            '{request.form["platform"]}',
            '{request.form["status"]}',
            '{request.form["multiplayer"]}',
            '{request.form["comments"]}',
            '{request.form["released"]}'
        )"""
    )
    db.commit()
    db.close()
    return game_list()


@BP_GAMES.route("/games/add")
def add():
    return render_template("add_game.html", title="Add a game")
