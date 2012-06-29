from models.db import db

def teardown_db():
    db.query("DROP TABLE songs")
    db.query("DROP TABLE votes")
    db.query("DROP TABLE sessions")

teardown_db()
