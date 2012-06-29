import sys, os
abspath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abspath)
sys.path.append("..")
os.chdir(abspath)

import web
import json

import models.songs
import models.votes

from voting_webapi import VoteWebapiController
from voting_webapi import StartWebapiController
from voting_scripting import VoteScriptingController
from voting_scripting import SongsController

VOTING_HOTLINE="+990009369996194333"

render = web.template.render('../templates/')

urls = (
        '/results.json', 'ResultsJsonController',
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
    for title, keyword, number, votes in models.songs.songs_array('votes_cache DESC'):
        html.append("<li>%s (%s votes) - to vote say '%s' or press %s</li>" % (title, votes, keyword, number))
    return "\n".join(html)

### @export "index"
class Index(object):
    def GET(self, name):
        return render.index(VOTING_HOTLINE, models.songs.songs_dict('votes_cache DESC'))

### @export "results-json"
class ResultsJsonController(object):
    def GET(self):
        return json.dumps(models.songs.songs_dict('votes_cache DESC'))

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
if __name__ == '__main__':

    app = web.application(urls, globals())

    if os.environ.has_key('PORT'):
        port = int(os.environ['PORT'])
    else:
        port = 8080

    server_address =("0.0.0.0", port)

    func = app.wsgifunc()
    func = web.httpserver.StaticMiddleware(func)

    server = web.httpserver.WSGIServer(server_address, func)
    try:
         server.start()
    except KeyboardInterrupt:
         server.stop()
