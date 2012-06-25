import sys, os
abspath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abspath)
sys.path.append("..")
os.chdir(abspath)

import web

import models.songs
import models.votes

from voting_webapi import VoteWebapiController
from voting_webapi import StartWebapiController
from voting_scripting import VoteScriptingController
from voting_scripting import SongsController

VOTING_HOTLINE="+990009369996194333"

render = web.template.render('../templates/')

urls = (
        '/results', 'ResultsController',
        '/songs.csv', 'SongsController',
        '/webapi/vote/(menu|response|confirm)', 'VoteWebapiController',
        '/webapi/vote/(confirm)/(.*)', 'VoteWebapiController',
        '/webapi/start', 'StartWebapiController',
        '/scripting/vote', 'VoteScriptingController',
        '/votes', 'Votes',
        '/(.*)', 'Index'
        )

def results_table():
    """
    Make it so we can share code between ajax and vanilla versions of results table.
    """
    html = []
    for title, votes in models.songs.results():
        html.append("<li>%s (%s votes)</li>" % (title, votes))
    return "\n".join(html)

### @export "index"
class Index(object):
    def GET(self, name):
        return render.index(VOTING_HOTLINE, results_table())

### @export "results"
class ResultsController(object):
    def GET(self):
        return results_table()

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
