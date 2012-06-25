### @export "imports"
import web

### @export "db"
# db path relative to app/ directory which will load this
db = web.database(dbn='sqlite', db='../data/data.sqlite3')

### @export "songs-array"
def songs_array():
    """
    Returns an array of information for each song in the database.
    """
    songs = []
    for row in db.select('songs', order='number'):
        songs.append((row['title'], row['keyword'], row['number'], row['votes_cache']))
    return songs

### @export "cache-vote"
def cache_vote(number):
    """
    Increments the cached votes for this song.
    """
    previous_votes_cache = db.select("songs", where="number=$number", vars=locals())[0]['votes_cache']
    if not previous_votes_cache:
        previous_votes_cache = 0
    db.update("songs", where="number=$number", votes_cache=previous_votes_cache+1, vars=locals())

### @export "song-title"
def song_title(number):
    """
    Returns the song title for a given song number.
    """
    return db.select("songs", where="number=$number", vars=locals())[0]["title"]
