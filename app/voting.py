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

VOTING_HOTLINE="+49 (0) 30 3080 8581"

render = web.template.render('../templates/')

urls = (
        '/results.json', 'ResultsJsonController',
        '/scripting/vote', 'VoteScriptingController',
        '/songs.csv', 'SongsController',
        '/votes', 'Votes',
        '/webapi/start', 'StartWebapiController',
        '/webapi/vote/(confirm)/(.*)', 'VoteWebapiController',
        '/webapi/vote/(menu|response|confirm)', 'VoteWebapiController',
        '/', 'Index'
        )

### @export "index"
class Index(object):
    def GET(self):
        return render.index(VOTING_HOTLINE, models.songs.songs_dict(order='votes_cache DESC, number ASC'))

### @export "results-json"
class ResultsJsonController(object):
    def GET(self):
        return json.dumps(models.songs.songs_dict(order='votes_cache DESC, number ASC'))

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
