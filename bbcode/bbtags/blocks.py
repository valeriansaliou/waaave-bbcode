from datetime import date
from bbcode import *
import re

# Pygments if available
try:
    from pygments import highlight
    from pygments.lexers import guess_lexer, get_lexer_by_name, TextLexer
    from pygments.util import ClassNotFound
    from bbcode.mypygments import CodeHtmlFormatter
except ImportError:
    highlight = None


class P(BlockReplaceTagNode):
    """
    Creates a paragraph.

    Usage:

    [code lang=bbdocs linenos=0][p]Text[/p][/code]
    """
    verbose_name = 'Paragraph'
    open_pattern = re.compile(patterns.no_argument % 'p')
    close_pattern = re.compile(patterns.closing % 'p')


class Quote(BlockTagNode):
    """
    Defines a quote.

    Usage:

    [code lang=bbdocs linenos=0][quote=content_id]Text[/quote][/code]
    """
    verbose_name = 'Quote'
    open_pattern = re.compile(r'(\[quote=(?P<content_id>[^\]]+)\])')
    close_pattern = re.compile(patterns.closing % 'quote')

    def get_quote(self, content_id):
        try:
            from _index.helpers import read_content_data
        except ImportError:
            return {}
        content_data = read_content_data(content_id)
        quote = {
            'author_avatar': content_data['author']['avatar'],
            'author_rank': content_data['author']['rank'],
            'author_name': '%s %s' % (content_data['author']['first_name'], content_data['author']['last_name']),
            'author_url': content_data['author']['url'],
            'author_specialty': content_data['author']['specialty'],
            'quote_page_url': content_data['content']['url'],
            'quote_page_title': content_data['content']['title']
        }
        return quote

    def build_html(self, content_id, content):
        quote = self.get_quote(content_id)
        return  u'<div class="quote-feature">'\
                    '<div class="avatar-wrapper wr{author_rank}">'\
                        '<div class="avatar">'\
                            '<a href="{author_url}">'\
                                '{author_avatar}'\
                                '<span class="label label-blue">{author_rank}</span>'\
                            '</a>'\
                        '</div>'\
                    '</div>'\
                    '<blockquote>'\
                        '<span class="quote-arrow"></span>'\
                        '&quot;{content}&quot;'\
                    '</blockquote>'\
                    '<div class="author">'\
                        '<a href="{author_url}" class="username">{author_name}</a>, <em>{author_specialty}</em>, in <a href="{quote_page_url}">{quote_page_title}</a>.'\
                    '</div>'\
                '</div>'.format(content=content,
                                author_avatar=quote.get('author_avatar', ''),
                                author_rank=quote.get('author_rank', 0),
                                author_url=quote.get('author_url', ''),
                                author_name=quote.get('author_name', ''),
                                author_specialty=quote.get('author_specialty', ''),
                                quote_page_url=quote.get('quote_page_url', ''),
                                quote_page_title=quote.get('quote_page_title', ''))

    def parse(self, as_text=False):
        gd = self.match.groupdict()
        content_id = gd.get('content_id', None)
        if content_id is None:
            return self.soft_raise("No article ID attached to the quote.")
        if as_text: return self.parse_inner(as_text)
        return self.build_html(content_id, self.parse_inner())


class Code(BlockTagNode):
    """
    Defines text as code (with highlighting).

    Usage:

    [code lang=bbdocs linenos=0][code=language]Your Code[/code][/code]

    Arguments:

    Allowed [i]languages[/i]: http://pygments.org/languages/ Default: autodetect
    """
    verbose_name = 'Code'
    open_pattern = re.compile(r'\[code\]|\[code=(?P<language>[^\]]+)\]')
    close_pattern = re.compile(patterns.closing % 'code')

    def __init__(self, parent, match, content, context):
        TagNode.__init__(self, parent, match, content, context)

        gd = match.groupdict()
        kwargs = {'language': ''}
        if 'language' in gd and gd['language']:
            kwargs['language'] = gd['language']
        self.arguments = kwargs

    def build_html(self, language, copyright, highlighted):
        code_counts = ''
        for i in range(1, highlighted.count('code-line') + 1):
            code_counts += u'<a href="#L{i}" rel="#L{i}">{i}</a>'.format(i=i)

        return  u'<div class="block-code" data-language="{language}" data-copyright="{copyright}">'\
                    '<div class="code-head">'\
                        '<span class="code-language">{language_title}</span>'\
                        '<a class="code-copy" href="#">'\
                            '<span class="code-copy-first">Copy to Clipboard</span>'\
                            '<span class="code-copy-done">Copied. Copy again?</span>'\
                        '</a>'\
                    '</div>'\
                    '<div class="code-content">'\
                        '<div class="code-counts">'\
                            '{counts}'\
                        '</div>'\
                        '<div class="code-lines">'\
                            '{highlighted}'\
                        '</div>'\
                    '</div>'\
                '</div>'.format(language=language, language_title=(language or 'code').title(), copyright=copyright, counts=code_counts, highlighted=highlighted)

    def parse(self, as_text=False):
        """
        pygment highlighting
        """
        inner = ''
        language = self.arguments['language']
        for node in self.nodes:
            inner += node.raw_content
        if highlight is None:
            return '<pre>%s</pre>' % inner
        if language:
            try:
                lexer = get_lexer_by_name(language)
            except ClassNotFound:
                try:
                    lexer = guess_lexer(inner)
                except ClassNotFound:
                    lexer = TextLexer()
        else:
            try:
                lexer = guess_lexer(inner)
            except ClassNotFound:
                lexer = TextLexer()
        copyright=u'(c) {year} Waaave - %s'.format(year=date.today().year)
        highlighted = highlight(inner, lexer, CodeHtmlFormatter())
        if as_text: return ''
        return self.build_html(language=language, copyright=copyright, highlighted=highlighted)


class Info(BlockReplaceTagNode):
    """
    Builds an information block

    Usage:

    [code lang=bbdocs linenos=0][info]Text[/info][/code]
    """
    verbose_name = 'Information Block'
    open_pattern = re.compile(patterns.no_argument % 'info')
    close_pattern = re.compile(patterns.closing % 'info')

    def build_html(self, name):
        return u'<div class="block-details block-{name}">'                             \
                   '<span class="icon-block icon-{name}"></span>'       \
                   '<span class="text-block text-{name}">{text}</span>' \
               '</div>'.format(name=name, text=self.parse_inner())

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.build_html('info')


class Danger(Info):
    """
    Builds a danger block

    Usage:

    [code lang=bbdocs linenos=0][danger]Text[/danger][/code]
    """
    verbose_name = 'Danger Block'
    open_pattern = re.compile(patterns.no_argument % 'danger')
    close_pattern = re.compile(patterns.closing % 'danger')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.build_html('danger')


class Warning(Info):
    """
    Builds a warning block

    Usage:

    [code lang=bbdocs linenos=0][warning]Text[/warning][/code]
    """
    verbose_name = 'Warning Block'
    open_pattern = re.compile(patterns.no_argument % 'warning')
    close_pattern = re.compile(patterns.closing % 'warning')

    def parse(self, as_text=False):
        if as_text: return self.parse_inner(as_text)
        return self.build_html('warning')


register(P)
register(Quote)
register(Code)
register(Info)
register(Danger)
register(Warning)
