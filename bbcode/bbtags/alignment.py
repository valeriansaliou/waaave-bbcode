from bbcode import *
import re


class Center(BlockReplaceTagNode):
    """
    Centers text.
    
    Usage:
    
    [code lang=bbdocs linenos=0][center]Text[/center][/code]
    """
    verbose_name = 'Center Text'
    open_pattern = re.compile(patterns.no_argument % 'center')
    close_pattern = re.compile(patterns.closing % 'center')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return u'<p class="ta-center">%s</p>' % self.parse_inner()


class Left(BlockReplaceTagNode):
    """
    Aligns text on the left.
    
    Usage:
    
    [code lang=bbdocs linenos=0][left]Text[/left][/code]
    """
    verbose_name = 'Align Text Left'
    open_pattern = re.compile(patterns.no_argument % 'left')
    close_pattern = re.compile(patterns.closing % 'left')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return u'<p class="ta-left">%s</p>' % self.parse_inner()


class Right(BlockReplaceTagNode):
    """
    Aligns text on the right.
    
    Usage:
    
    [code lang=bbdocs linenos=0][right]Text[/right][/code]
    """
    verbose_name = 'Align Text Right'
    open_pattern = re.compile(patterns.no_argument % 'right')
    close_pattern = re.compile(patterns.closing % 'right')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return u'<p class="ta-right">%s</p>' % self.parse_inner()


class Justify(BlockReplaceTagNode):
    """
    Justifies text.
    
    Usage:
    
    [code lang=bbdocs linenos=0][justify]Text[/justify][/code]
    """
    verbose_name = 'Justify Text'
    open_pattern = re.compile(patterns.no_argument % 'justify')
    close_pattern = re.compile(patterns.closing % 'justify')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return u'<p class="ta-justify">%s</p>' % self.parse_inner()


register(Center)
register(Left)
register(Right)
register(Justify)