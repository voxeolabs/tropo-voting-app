import web
import models.songs

# db path relative to app/ directory which will load this
db = web.database(dbn='sqlite', db='../data/data.sqlite3')

### @export "vote-for-song"
def vote_for_song(song_number, phone_number):
    """
    Insert a vote and increment the cache.
    """
    db.insert('votes', song_number=song_number, phone_number=phone_number)
    models.songs.cache_vote(song_number)
    return song_number

### @export "votes"
def votes_array():
    votes = []
    for row in db.select('votes', order='id'):
        votes.append([row['id'], row['song_number'], row['phone_number']])
    return votes
