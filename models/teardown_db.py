from models.db import db

def teardown_db():
    db.query("DROP TABLE if exists songs")
    db.query("DROP TABLE if exists votes")
    db.query("DROP TABLE if exists sessions")

teardown_db()
