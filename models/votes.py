import web
import re
import models.songs
from models.sessions import session_info

db = web.database(dbn='postgres', host='localhost',  db='voting')

def caller_id_if_valid(tropo_call_id):
    session = session_info(tropo_call_id)
    is_skype = session['caller_network'] in ('SKYPE')
    is_numeric_phone_channel = session['caller_network'] in ('SIP', 'SMS')
    is_number = re.match("^(\+)?[0-9]+$", session['caller_id'])
    if (is_numeric_phone_channel and is_number) or is_skype:
        return session['caller_id']
    else:
        web.debug("channel is %s" % session['caller_network'])
        web.debug("caller id is %s" % session['caller_id'])
        return None

def caller_id_can_vote(caller_id):
    is_number = re.match("^(\+)?[0-9]+$", caller_id)
    if caller_id:
        return count_votes_by_caller_id(caller_id) == 0 or not is_number
    else:
        return False

def count_votes_by_caller_id(caller_id):
    results = db.query("SELECT COUNT(*) as count_votes from votes WHERE phone_number=$caller_id", vars=locals())
    return int(results[0].count_votes)

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
