from bbcode import *
import re
import urllib
from urlparse import urlparse
from django.conf import settings


class Url(TagNode):
    """
    Creates a hyperlink.
    
    Usage:
     
    [code lang=bbdocs linenos=0][url=<http://www.domain.com>]Text[/url]
[url]http://www.domain.com[/url][/code]
    """
    verbose_name = 'Link'
    open_pattern = re.compile(r'(\[url\]|\[url="?(?P<href>[^\]]+)"?\]|\[url (?P'
                               '<arg1>\w+)="?(?P<val1>[^ ]+)"?( (?P<arg2>\w+)="'
                               '?(?P<val2>[^ ]+)"?)?\])')
    close_pattern = re.compile(patterns.closing % 'url')
    
    def parse(self, as_text=False):
        gd = self.match.groupdict()
        gd.update({'css':''})
        if gd['arg1']:
            gd[gd['arg1']] = gd['val1']
        if gd['arg2']:
            gd[gd['arg2']] = gd['val2']
        if gd['href']:
            href = self.variables.resolve(gd['href'])
            inner = self.parse_inner(as_text)
        else:
            inner = ''
            for node in self.nodes:
                if node.is_text_node or isinstance(node, AutoDetectURL):
                    inner += node.raw_content
                else:
                    self.soft_raise("Url tag cannot have nested tags without "
                                    "an argument.")
            href = self.variables.resolve(inner)
            inner = href
        if gd['css']:
            css = ' class="%s"' % gd['css'].replace(',',' ')
        else:
            css = ''
        raw_href = self.variables.resolve(href)

        # url escape
        raw_href = urlparse(raw_href)
        path =  raw_href.netloc + raw_href.path
        if raw_href.params:
            path += ";" + raw_href.params
        if raw_href.query:
            path += "?" + raw_href.query
        if raw_href.fragment:
            path += "#" + raw_href.fragment
        href_escaped = raw_href.scheme + "://" + urllib.quote(path)

        css = self.variables.resolve(css)
        if as_text: return inner
        return u'<a target="_blank" href="%s"%s>%s</a>' % (href_escaped, css, inner)
    

class Email(TagNode):
    """
    Creates an email link.
    
    Usage:
    
    [code lang=bbdocs linenos=0][email]name@domain.com[/email]
[email=<name@domain.com>]Text[/email][/code]
    """
    verbose_name = 'E-Mail'
    open_pattern = re.compile(r'(\[email\]|\[email=(?P<mail>[^\]]+\]))')
    close_pattern = re.compile(patterns.closing % 'email')

    def parse(self, as_text=False):
        gd = self.match.groupdict()
        email = gd.get('email', None)
        if as_text: return email
        if email:
            inner = ''
            for node in self.nodes:
                if node.is_text_node or isinstance(node, AutoDetectURL):
                    inner += node.raw_content
                else:
                    inner += node.parse()
            return u'<a href="mailto:%s">%s</a>' % (email, inner)
        else:
            inner = ''
            for node in self.nodes:
                inner += node.raw_content
            return u'<a href="mailto:%s">%s</a>' % (inner, inner)
    
    

    
    
class Img(ArgumentTagNode):
    """
    Displays an image.
    
    Usage:
    
    [code lang=bbdocs linenos=0][img]http://www.domain.com/image.jpg[/img]
[img=<align>]http://www.domain.com/image.jpg[/img][/code]
    
    Arguments:
    
    Allowed values for [i]align[/i]: left, center, right. Default: None.
    """
    verbose_name = 'Image'
    open_pattern = re.compile(patterns.single_argument % 'img')
    close_pattern = re.compile(patterns.closing % 'img')
    
    def parse(self, as_text=False):
        inner = ''
        if as_text: return inner
        for node in self.nodes:    
            if node.is_text_node or isinstance(node, AutoDetectURL):
                inner += node.raw_content
            else:
                soft_raise("Img tag cannot have nested tags without an argument.")
                return self.raw_content
        inner = self.variables.resolve(inner)
        image_url = '%s/%s' % (settings.MEDIA_URL.strip('/'), inner.strip('/'),)
        if self.argument:
            return u'<img src="%s" alt="image" class="img-%s" />' % (image_url, self.argument)
        else:
            return u'<img src="%s" alt="image" />' % image_url
    
    
class Youtube(BlockTagNode):
    """
    Includes a youtube video. Post the URL to the youtube video inside the tag.
    
    Usage:
    
    [code lang=bbdocs linenos=0][youtube]http://www.youtube.com/watch?v=FjPf6B8EVJI[/youtube][/code]
    """
    _video_id_pattern = re.compile('v=(\w+)')
    open_pattern = re.compile(patterns.no_argument % 'youtube')
    close_pattern = re.compile(patterns.closing % 'youtube')
    
    def parse(self, as_text=False):
        url = ''
        if as_text: return url
        for node in self.nodes:
            if node.is_text_node or isinstance(node, AutoDetectURL):
                inner += node.raw_content
            else:
                soft_raise("Youtube tag cannot have nested tags")
                return self.raw_content
        match = self._video_id_pattern.search(url)
        if not match:
            soft_raise("'%s' does not seem like a youtube link" % url)
            return self.raw_content
        videoid = match.groups()
        if not videoid:
            soft_raise("'%s' does not seem like a youtube link" % url)
            return self.raw_content
        videoid = videoid[0]
        return (
            u'<object width="560" height="340"><param name="movie" value="http:/'
            '/www.youtube.com/v/%s&amp;hl=en&amp;fs=1&amp;"></param><param name'
            '="allowFullScreen" value="true"></param><param name="allowscriptac'
            'cess" value="always"></param><embed src="http://www.youtube.com/v/'
            '%s&amp;hl=en&amp;fs=1&amp;" type="application/x-shockwave-flash" a'
            'llowscriptaccess="always" allowfullscreen="true" width="560" heigh'
        )


class Download(BlockTagNode):
    """
    Creates a download link.
    
    Usage:
     
    [code lang=bbdocs linenos=0][download=<file_path>]Download Title[/url][/code]
    """
    verbose_name = 'Download'
    open_pattern = re.compile(r'(\[download="?(?P<path>[^\]]+)"?\])')
    close_pattern = re.compile(patterns.closing % 'download')
    
    def parse(self, as_text=False):
        if as_text: return ''
        gd = self.match.groupdict()
        if not gd['path']:
            return self.soft_raise("Download tag must have a file path attribute.")
        path = self.variables.resolve(gd['path'])
        path_absolute = '%s/%s' % (settings.MEDIA_URL.strip('/'), path.strip('/'),)
        title = self.parse_inner(as_text)
        return u'<div class="block-details block-download">'                                                                             \
                  '<span class="icon-block"></span>'                                                                      \
                  '<span class="text-block">Click on the following link to download <a href="{path}">{title}</a>.</span>' \
                  '<div class="clear"></div>'                                                                             \
               '</div>'.format(path=path_absolute, title=title)

    
class AutoDetectURL(SelfClosingTagNode):
    open_pattern = re.compile('((ht|f)tps?:\/\/([-\w\.]+)+(:\d+)?(\/([\w\/_\.,-]*(\?\S+)?)?)?)')

    def parse(self, as_text=False):
        url = self.match.group()
        if as_text: return url
        return u'<a href="%s">%s</a>' % (url, url)
    

register(Url)
register(Img)
register(Email)
register(Youtube)
register(Download)
register(AutoDetectURL)