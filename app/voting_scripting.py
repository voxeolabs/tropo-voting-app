import StringIO
import csv
import models.songs
import models.votes
import web

### @export "songs"
class SongsController(object):
    def GET(self):
        songs_array = models.songs.songs_array()
        output = StringIO.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer.writerows(songs_array)
        return output.getvalue()

### @export "vote"
class VoteScriptingController(object):
    def POST(self):
        pairs = web.data().split("&")
        data = {}
        for s in pairs:
            k, v = s.split("=")
            data[k] = v

        song_number = int(data["song"])
        models.votes.vote_for_song(song_number, data["from"])
        song_title = models.songs.song_title(song_number)
        return "You voted for song: %s" % song_title
