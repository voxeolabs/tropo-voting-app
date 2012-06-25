import sys, os
abspath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abspath)
sys.path.append("..")
os.chdir(abspath)

import web

import csv
import StringIO

import models.songs
import models.votes

urls = (
        '/songs.csv', 'Songs',
        '/vote', 'Vote',
        '/votes', 'Votes',
        '/(.*)', 'Index'
        )

### @export "index"
class Index(object):
    def GET(self, name):
        web.header('Content-Type', 'text/html')
        html = []
        html.append("""
        <pre>
        Phone Numbers:
        Skype Voice: +990009369996171439
        SIP Voice: sip:9996171439@sip.tropo.com
        INum Voice: +883510001187547
        Phono App Address: app:9996171439
        </pre>
        """)
        html.append("<table>\n<tr><th>Song</th><th>Votes</th></tr>")
        for title, keyword, number, votes in models.songs.songs_array():
            html.append("<tr><td>%s</td><td>%s</td></tr>" % (title, votes))
        html.append("</table>")
        html.append("""<p><a href="/docs">docs</a></p>""")
        return "\n".join(html)

### @export "songs"
class Songs(object):
    def GET(self):
        songs_array = models.songs.songs_array()
        output = StringIO.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer.writerows(songs_array)
        return output.getvalue()

### @export "vote"
class Vote(object):
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

### @export "votes"
class Votes(object):
    def GET(self):
        web.header('Content-Type', 'text/html')
        html = []
        html.append("<pre>")
        for vote_id, song_number, phone_number in models.votes.votes_array():
            song_title = models.songs.song_title(song_number)
            html.append("Person calling from %s voted for %s (#%s)" % (phone_number, song_title, song_number))
        html.append("</pre>")
        return "\n".join(html)

### @export "start-app"
app = web.application(urls, globals())
application = app.wsgifunc()
