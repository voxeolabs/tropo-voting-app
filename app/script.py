### @export "imports"
import urllib2
import csv

### @export "greeting"
say("hello, thank you for helping us choose the music")

### @export "constants"
APP_URL = "http://voice.pitchlift.org"
SONGS_DATA = "%s/songs.csv" % APP_URL
VOTE_URL = "%s/vote" % APP_URL

### @export "load-songs"
songs_url = urllib2.urlopen(SONGS_DATA)
songs_array = csv.reader(songs_url)

### @export "song-prompt"
prompts = []
choices = []
for title, keyword, number, votes_cache in songs_array:
    choices.append("%s(%s,%s)" % (number, keyword, number))
    prompts.append("For %(title)s, say %(keyword)s or press %(number)s." % locals())
prompt = " ".join(prompts)

### @export "prompt-user"
result = ask(prompt, {'choices' : ",".join(choices) })

### @export "post-vote"
if result.name == "choice":
    vote_response = urllib2.urlopen(VOTE_URL, "song=%s&from=%s" % (result.value, currentCall.callerID))
    say(vote_response.read())
