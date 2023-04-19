from bsky_bot.bsky import Bsky, Skoot
from typing import List

class Bot:
    def __init__(self, bsky: Bsky)->None:
        self.bsky = bsky
        self.options ={
            '-h':('returns available options',self._help),
            '-x':('deletes parent skoot of reply',self._delete)
        }

    def execute(self)->None:
        replies, likes, followers = self.bsky.get_notifications()
        for r in replies:
            self.parse_reply(r)

    def parse_reply(self, skoot:Skoot) ->None:
        args = skoot.text.strip().split(' ')
        for i in args:
            if i in self.options:
                fxn = self.options[i][1]
                fxn(skoot)        

    def _help(self, skoot:Skoot)->None:      
        x = ''
        for k, v in self.options.items():
            x+=f'{k}: {v[0]}\n'
        skoot.reply(x)
    
    def _delete(self, skoot:Skoot)->None:
        skoot.delete(skoot.parent)

