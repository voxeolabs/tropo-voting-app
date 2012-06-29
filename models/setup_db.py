from models.db import db

def setup_db():
    db.query("CREATE TABLE songs (number integer PRIMARY KEY, title varchar(100), keyword varchar(50), votes_cache integer)")
    db.query("CREATE TABLE votes (id SERIAL PRIMARY KEY, song_number integer, phone_number varchar(50))")
    db.query("CREATE TABLE sessions (tropo_call_id varchar(100), caller_network varchar(20), caller_channel varchar(20), caller_id varchar(50))")

    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Piano Man by Billy Joel", "piano", 1);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Imagine by John Lennon", "imagine", 2);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Tiny Dancer by Elton John", "dancer", 3);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Crazy Little Thing Called Love by Queen", "crazy", 4);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Daydream Believer by The Monkees", "daydream", 5);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Sweet Caroline by Neil Diamond", "caroline", 6);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Hey Jude by The Beatles", "jude", 7);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Don't Stop Believin by Journey", "believing", 8);""")
    db.query("""INSERT INTO songs (title, keyword, number) VALUES ("Tainted Love by Soft Cell", "tainted", 9);""")

setup_db()
