from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd

from urllib import urlencode
from urllib2 import Request, urlopen

import re


class Translate(BotPlugin):

    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'client': 't', 'sl': None, 'tl': None, 'text': None}
    url = 'http://translate.google.com/translate_a/t'

    @botcmd
    def translate(self, mess, args):
        """Translate a string from a certain source language to a target language.
        Example: !translate en fr computer
        """
        self.params['sl'], self.params['tl'], self.params['text'] = args.strip().split()
        request = Request(self.url, urlencode(self.params), self.headers)
        raw_response = urlopen(request).read()

        # The response we're getting from the API often has invalid syntax,
        # removing duplicate commas seems to fix it.
        response = eval(re.sub(r',,+', ',', raw_response))
        try:
            return response[0][0][0]
        except IndexError:
            return 'Failed to perform translation.'