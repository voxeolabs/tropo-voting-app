from tropo import Tropo, Choices, Result
import json
import re
import web
import models.songs
import models.sessions
import models.votes

### @export "base-webapi-controller"
class BaseWebapiController(object):
    """
    Defines some convenience methods.
    """
    def call_id(self):
        data = json.loads(web.data())
        if data.has_key('session'):
            return data['session']['callId']
        elif data.has_key('result'):
            return data['result']['callId']
        else:
            print data
            print data.keys()
            raise Exception("Can't obtain call id, have no session or result")

    def get_result(self):
        return Result(web.data())

    def get_answer(self):
        """
        Retrieves the user-supplied value after an 'ask'
        """
        r = self.get_result()
        try:
            return r.getValue()
        except KeyError:
            return None

### @export "menu-webapi-controller"
class MenuWebapiController(BaseWebapiController):
    """
    Base class for menu-driven controllers which follow a 'prompt, get response,
    confirm response' pattern.
    """
    URL_ROOT = "base"

    def url_root(self):
        return self.URL_ROOT

    def menu_url(self):
        return "/%s/%s" % (self.url_root(), "menu")

    def confirm_url(self, arg=None):
        if arg:
            return "/%s/%s/%s" % (self.url_root(), "confirm", arg)
        else:
            return "/%s/%s" % (self.url_root(), "confirm")

    def confirm_choices(self):
        return Choices("yes (1), no (2)", mode="dtmf")

    def confirm_prompt(self):
        return "Press 1 for yes. Press 2 for no."

    def response_url(self):
        return "/%s/%s" % (self.url_root(), "response")

    def POST(self, name, arg=None):
        web.header('Content-Type', 'text/json')
        if name == 'menu':
            return self.do_menu()
        elif name == 'response':
            return self.do_response()
        elif name == 'confirm':
            answer = self.get_answer()
            if answer == 'yes':
                return self.do_confirm_ok(arg)
            else:
                return self.do_bad_choice("Okay, let's try again")
        else:
            raise Exception("don't know how to do action %s" % name)

    def do_bad_choice(self, message="Sorry, that's not a valid choice."):
        t = Tropo()
        t.say(message)
        t.on(event = "continue", next=self.menu_url())
        return t.RenderJson()

### @export "vote-webapi-controller"
class VoteWebapiController(MenuWebapiController):
    URL_ROOT = 'webapi/vote'

### @export "do-menu"
    def do_menu(self):
        t = Tropo()
        t.say("hello, thank you for helping us choose the music")

        prompts = []
        choices = []
        for title, keyword, number, votes_cache in models.songs.songs_array():
            choices.append("%s(%s,%s)" % (number, keyword, number))
            prompts.append("For %(title)s, press %(number)s." % locals())
        prompt = " ".join(prompts)

        t.ask(Choices(",".join(choices)), mode="dtmf", say=prompt)
        t.on(event="continue", next=self.response_url())
        return t.RenderJson()

### @export "do-response"
    def do_response(self):
        song_id = self.get_answer()
        song_title = models.songs.song_title(song_id)

        if not song_id:
            return self.do_bad_choice()
        else:
            t = Tropo()
            prompt = "You chose %s, is that correct? " % song_title
            choices = self.confirm_choices()
            t.ask(choices, say=prompt + self.confirm_prompt())
            t.on(event="continue", next=self.confirm_url(song_id))
            return t.RenderJson()

    def do_confirm_ok(self, song_id):
        caller_id = models.votes.caller_id_if_valid(self.call_id())
        models.votes.vote_for_song(song_id, caller_id)
        t = Tropo()
        t.say("Great, your vote has been counted. Goodbye.")
        t.message("Thanks for voting!", channel="TEXT", to=caller_id)
        return t.RenderJson()

### @export "start"
class StartWebapiController(BaseWebapiController):
    def do_voice(self):
        t = Tropo()

        caller_id = models.votes.caller_id_if_valid(self.call_id())
        web.debug("starting to handle voice call from %s" % caller_id)

        if models.votes.caller_id_can_vote(caller_id):
            t.on(event="continue", next="/webapi/vote/menu")
        elif not caller_id:
            t.say("Oops, you need to have caller eye dee enabled to vote. Goodbye.")
            t.hangup()
        else:
            t.say("Oops, it looks like you have voted already. Goodbye.")
            t.hangup()

        return t.RenderJson()

    def GET(self):
       return "<p>This method isn't that interesting unless tropo is calling it.</p>"

    def POST(self):
        web.debug(web.data())

        # save session info for this call
        session_info = json.loads(web.data())['session']

        tropo_call_id = session_info['callId']
        caller_network = session_info['from']['network']
        caller_channel = session_info['from']['channel']
        caller_id = session_info['from']['id']

        models.sessions.new_session(
                tropo_call_id,
                caller_network,
                caller_channel,
                caller_id)

        if caller_channel == 'VOICE':
            return self.do_voice()
        else:
            raise Exception("unexpected caller channel %s" % caller_channel)

