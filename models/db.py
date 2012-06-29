import web
import os
import dj_database_url

def parse_db_url():
    # assumes heroku config where db info is specifid in environment variable named DATABASE_URL
    database_url = os.environ["DATABASE_URL"]
    params = dj_database_url.parse(database_url)
    return web.database(dbn='postgres', host=params['HOST'], db=params['NAME'], user=params['USER'], pw=params['PASSWORD'])

def initialize_db():
    db.query("CREATE TABLE songs (number integer PRIMARY KEY)")

def reset_db():
    db.query("DROP TABLE songs")

db = parse_db_url()
reset_db()
