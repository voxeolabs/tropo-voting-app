from models.db import db

def setup_db():
    db.query("CREATE TABLE songs (number integer PRIMARY KEY, title varchar(100), keyword varchar(50), votes_cache integer)")
    db.query("CREATE TABLE votes (id SERIAL PRIMARY KEY, song_number integer, phone_number varchar(50))")
    db.query("CREATE TABLE sessions (tropo_call_id varchar(100), caller_network varchar(20), caller_channel varchar(20), caller_id varchar(50))")

    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Piano Man by Billy Joel', 'piano', 1, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Imagine by John Lennon', 'imagine', 2, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Tiny Dancer by Elton John', 'dancer', 3, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Crazy Little Thing Called Love by Queen', 'crazy', 4, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Daydream Believer by The Monkees', 'daydream', 5, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Sweet Caroline by Neil Diamond', 'caroline', 6, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Hey Jude by The Beatles', 'jude', 7, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Don\\'t Stop Believin by Journey', 'believing', 8, 0);")
    db.query("INSERT INTO songs (title, keyword, number, votes_cache) VALUES ('Tainted Love by Soft Cell', 'tainted', 9, 0);")

setup_db()
