import web

db = web.database(dbn='sqlite', db='../data/data.sqlite3')

def new_session(tropo_call_id, caller_network, caller_channel, caller_id):
    db.insert('sessions', **locals())

def session_info(tropo_call_id):
    return db.select('sessions', where='tropo_call_id=$tropo_call_id', vars=locals())[0]

