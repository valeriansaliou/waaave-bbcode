from bbcode import *
import re


class OL(BlockMultiArgumentTagNode):
    """
    Creates an ordered list.
    
    Usage:
    
    [code lang=bbdocs linenos=0][ol]
  [*] First item
  [*] Second item
[/ol][/code]
    """
    _arguments = {'css': '',
                  'itemcss': ''}
    
    @staticmethod
    def open_pattern():
        pat = r'\[ol'
        for arg in OL._arguments:
            pat += patterns.argument
        pat += r'\]'
        return re.compile(pat)
    
    close_pattern = re.compile(patterns.closing % 'ol')
    verbose_name = 'Ordered List'
    
    def list_parse(self, as_text=False):
        # Parse list items ([*])
        if self.arguments.itemcss:
            css = ' class="%s"' % self.arguments.itemcss.replace(',',' ')
        else:
            css = ''
        items = self.parse_inner(as_text).split('[*]')[1:]
        real = ''
        if as_text:
            for item in items: real += '- %s' % item
        else:
            for item in items: real += '<li%s>%s</li>' % (css, item)
        return real
        
    def parse(self, as_text=False):
        if as_text: return self.list_parse(as_text)
        if self.arguments.css:
            css = ' class="%s"' % self.arguments.css.replace(',',' ')
        else:
            css = ''
        return u'<ol%s>%s</ol>'  % (css, self.list_parse())


class UL(OL):
    """
    Creates an unordered list.
    
    Usage:
    
        [code lang=bbdocs linenos=0][ul]
  [*] First item
  [*] Second item
[/ul][/code]
    """
    @staticmethod
    def open_pattern():
        pat = r'\[ul'
        for arg in UL._arguments:
            pat += patterns.argument
        pat += r'\]'
        return re.compile(pat)
    close_pattern = re.compile(patterns.closing % 'ul') 
    verbose_name = 'Unordered List'
    
    def parse(self, as_text=False):
        if as_text: return self.list_parse(as_text)
        if self.arguments.css:
            css = ' class="%s"' % self.arguments.css.replace(',',' ')
        else:
            css = ''
        return u'<ul%s>%s</ul>'  % (css, self.list_parse())

class Steps(BlockTagNode):
    """
    Defines a steps list. Does not contain any text
    other than [step]...[/step] tags.
    
    Usage:
        
    [code lang=bbdocs linenos=0][steps]
  [step=1]text[/step]
[/steps][/code]
    """
    open_pattern = re.compile(patterns.no_argument % 'steps')
    close_pattern = re.compile(patterns.closing % 'steps')
    
    def parse(self, as_text=False):
        inner = ''
        for node in self.nodes:
            if isinstance(node, Step):
                inner += node.parse()
            elif node.raw_content.strip():
                soft_raise("Only step elements are allowed directly nested inside a steps element")
        if as_text: return inner
        return u'<div class="steps">%s</div>' % inner


class Step(BlockTagNode):
    """
    Defines a single step. Only allowed inside [code lang=bbdocs linenos=0][steps]...[/steps][/code]. 
    
    Usage:
    
    [code lang=bbdocs linenos=0][step=<number>]text[/step][/code]
    
    Arguments:
    
    [i]number[/i]: must be digit. Default: 1 (normal)
    """
    open_pattern = re.compile(r'(\[step\]|\[step="?(?P<argument>[^]]+)?"?\])')
    close_pattern = re.compile(patterns.closing % 'step')
    
    def __init__(self, parent, match, content, context):
        try:
            self.argument = match.group('argument').strip('"')
        except:
            self.argument = None
        TagNode.__init__(self, parent, match, content, context)
    
    def parse(self, as_text=False):
        step_num = 1
        if not isinstance(self.parent, Steps):
            soft_raise("Step are only allowed within a steps list!")
            return self.raw_content
        if self.argument:
            if self.argument.isdigit():
                step_num = self.argument
            else:
                soft_fail("Step argument must be digit")
        if as_text:
            return '%s. %s' % (step_num, self.parse_inner(as_text))
        return u'<div class="step">'               \
                  '<span class="key">%s</span>'   \
                  '<span class="value">%s</span>' \
                  '<div class="clear"></div>'     \
               '</div>' % (step_num, self.parse_inner())

register(OL)
register(UL)
register(Steps)
register(Step)