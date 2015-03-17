from bbcode import *
import re


class Emoticon(SelfClosingTagNode):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'em_name'):
            self.em_name = self.__class__.__name__.lower()
        SelfClosingTagNode.__init__(self, *args, **kwargs)

    def parse(self, as_text=False):
        if as_text: return ''
        return u'<span class="emoticon emoticon-%s"></span>' % self.em_name


class Smiling(Emoticon):
    # :), :-)
    open_pattern = re.compile(':-?\)')

class Blink(Emoticon):
    # ;), ;-)
    open_pattern = re.compile(';-?\)')

class Laughing(Emoticon):
    # :D, :-D
    open_pattern = re.compile(':-?D')

class Yuck(Emoticon):
    # :P, :-P
    open_pattern = re.compile(':-?(P|p)')

class Sad(Emoticon):
    # :(, :-(
    open_pattern = re.compile(':-?\(')

class Embarrassed(Emoticon):
    # :S, :-S
    open_pattern = re.compile(":-?(S|s)")

class Slant(Emoticon):
    # :/, :-/
    open_pattern = re.compile(":-?\/")

class Ambivalent(Emoticon):
    # :|, :-|
    open_pattern = re.compile(":-?\|")

class NotAmused(Emoticon):
    # --', --"
    open_pattern = re.compile("--(\'|\")")

class Crying(Emoticon):
    # :'(, :'-(
    open_pattern = re.compile(':-?\'\(')

class Cool(Emoticon):
    # B), B-)
    open_pattern = re.compile('B-?\)')

class Angry(Emoticon):
    # :@, :-@
    open_pattern = re.compile(':-?@')

class Naughty(Emoticon):
    # 3:), 3:-)
    open_pattern = re.compile('3:-?\)')

class Angel(Emoticon):
    # o:), o:-)
    open_pattern = re.compile('o:-?\)')

class Nerd(Emoticon):
    # 8), 8-)
    open_pattern = re.compile('8-?\)')

class MoneyMouth(Emoticon):
    # :$, :-$
    open_pattern = re.compile(':-?\$')

class ThumbsUp(Emoticon):
    # :+1:
    open_pattern = re.compile(':\+1:')

class ThumbsDown(Emoticon):
    # :-1:
    open_pattern = re.compile(':-1:')


register(Smiling)
register(Blink)
register(Laughing)
register(Yuck)
register(Sad)
register(Embarrassed)
register(Slant)
register(Ambivalent)
register(NotAmused)
register(Crying)
register(Cool)
register(Angry)
register(Naughty)
register(Angel)
register(Nerd)
register(MoneyMouth)
register(ThumbsUp)
register(ThumbsDown)