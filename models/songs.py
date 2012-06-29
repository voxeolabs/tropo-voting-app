### @export "imports"
import web

### @export "db"
db = web.database(dbn='postgres', host='localhost',  db='voting')

def songs_dict(order='number'):
    """
    Returns an array of songs with each song's info in a dict.
    """
    songs = []
    position = 0
    for row in db.select('songs', order=order):
        songs.append({
            'position' : position,
            'title' : row['title'],
            'keyword' : row['keyword'],
            'number' : row['number'],
            'votes' : row['votes_cache'] or 0
        })
        position += 1
    return songs

### @export "songs-array"
def songs_array(order='number'):
    """
    Returns an array of information for each song in the database.
    """
    songs = []
    for row in db.select('songs', order=order):
        votes = row['votes_cache'] or "0"
        songs.append((row['title'], row['keyword'], row['number'], votes))
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
