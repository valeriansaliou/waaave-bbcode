from bbcode import *
import re


class Em(ReplaceTagNode):
    """
    Makes text italic.
    
    Usage:
    
    [code lang=bbdocs linenos=0][i]Text[/i][/code]
    """
    verbose_name = 'Italic'
    open_pattern = re.compile(patterns.no_argument % 'i')
    close_pattern = re.compile(patterns.closing % 'i')


class Strong(ReplaceTagNode):
    """
    Makes text bold.
    
    Usage:
    
    [code lang=bbdocs linenos=0][b]Text[/b][/code]
    """
    verbose_name = 'Bold'
    open_pattern = re.compile(patterns.no_argument % 'b')
    close_pattern = re.compile(patterns.closing % 'b')


class U(ReplaceTagNode):
    """
    Underlines text.
    
    Usage:
    
    [code lang=bbdocs linenos=0][u]Text[/u][/code]
    """
    verbose_name = 'Underline'
    open_pattern = re.compile(patterns.no_argument % 'u')
    close_pattern = re.compile(patterns.closing % 'u')


class H1(BlockArgumentTagNode):
    """
    Turns a text into a first-level title
    
    Usage:
    
    [code lang=bbdocs linenos=0][h1]Text[/h1][/code]
    """
    vebose_name = 'H1 Heading'
    open_pattern = re.compile(patterns.single_argument % 'h1')
    close_pattern = re.compile(patterns.closing % 'h1')

    def heading(self, level):
        return u'<h%s>%s</h%s>' % (level, self.parse_inner(), level)

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.heading(1)


class H2(H1):
    """
    Turns a text into a second-level title
    
    Usage:
    
    [code lang=bbdocs linenos=0][h2]Text[/h2][/code]
    """
    vebose_name = 'H2 Heading'
    open_pattern = re.compile(patterns.single_argument % 'h2')
    close_pattern = re.compile(patterns.closing % 'h2')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.heading(2)


class H3(H1):
    """
    Turns a text into a third-level title
    
    Usage:
    
    [code lang=bbdocs linenos=0][h3]Text[/h3][/code]
    """
    vebose_name = 'H3 Heading'
    open_pattern = re.compile(patterns.single_argument % 'h3')
    close_pattern = re.compile(patterns.closing % 'h3')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.heading(3)


class H4(H1):
    """
    Turns a text into a fourth-level title
    
    Usage:
    
    [code lang=bbdocs linenos=0][h4]Text[/h4][/code]
    """
    vebose_name = 'H4 Heading'
    open_pattern = re.compile(patterns.single_argument % 'h4')
    close_pattern = re.compile(patterns.closing % 'h4')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.heading(4)


class H5(H1):
    """
    Turns a text into a fifth-level title
    
    Usage:
    
    [code lang=bbdocs linenos=0][h5]Text[/h5][/code]
    """
    vebose_name = 'H5 Heading'
    open_pattern = re.compile(patterns.single_argument % 'h5')
    close_pattern = re.compile(patterns.closing % 'h5')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.heading(5)


class H6(H1):
    """
    Turns a text into a sixth-level title
    
    Usage:
    
    [code lang=bbdocs linenos=0][h6]Text[/h6][/code]
    """
    vebose_name = 'H6 Heading'
    open_pattern = re.compile(patterns.single_argument % 'h6')
    close_pattern = re.compile(patterns.closing % 'h6')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.heading(6)


register(Em)
register(Strong)
register(U)
register(H1)
register(H2)
register(H3)
register(H4)
register(H4)
register(H5)