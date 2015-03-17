from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import striptags, force_escape

bbmodule = __import__('bbcode',level=0)

register = template.Library()

class PseudoVar(object):
    def __init__(self, content):
        self.content = content
        self.var = content
        
    def resolve(self, context):
        return self.content


class BBCodeNode(template.Node):
    def __init__(self, content, namespaces, varname, as_text=False):
        self.content = template.Variable(content)
        self.namespaces = []
        for ns in namespaces:
            if ns[0] == ns[-1] and ns[0] in ('"',"'"):
                self.namespaces.append(PseudoVar(ns[1:-1]))
            else:
                self.namespaces.append(template.Variable(ns))
        self.as_text = as_text
        self.varname = varname

    def render(self, context):
        try:
            content = self.content.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        namespaces = set()
        for obj in self.namespaces:
            ns = obj.resolve(context)
            if type(ns) in (list, tuple):
                namespaces = namespaces.union(ns)
            else:
                namespaces.add(ns)
        parsed, errors = bbmodule.parse(content, namespaces, False, True, context, self.as_text)
        if self.varname:
            context[self.varname] = mark_safe(parsed)
            return ''
        else:
            return mark_safe(parsed)

def parse(content, as_text=False):
    parsed, errors = bbmodule.parse(content, strict=True, auto_discover=True, as_text=as_text)
    return mark_safe(parsed)

@register.filter(name='bbcode')
def bbcode_filter(content):
    return parse(content)

@register.filter(name='bbcode_as_text')
def bbcode_filter_as_text(content):
    return parse(content, as_text=True)

@register.tag
def bbcode(parser, token):
    """
    Parses a context with the bbcode markup.
    
    Usage:
        
        {% bbcode <content> [<namespace1>, [<namespace2>...]] %}
        
    Params:
    
        <content> either a string of content or a template variable holding the
        content.
        
        <namespaceX> either a string or a template variable holding a string,
        list or tuple.
    
    WARNING: Errors are explicitly silenced in this tag because errors should be
    raised when 'content' is saved to the database (or where ever it is saved to).
    
    Please use bbcode.validate(...) on your content before saving it.
    """
    bbmodule.autodiscover()
    bits = token.contents.split()
    tag_name = bits.pop(0)
    try:
        content = bits.pop(0)
    except ValueError:
        raise template.TemplateSyntaxError("bbcode tag requires at least one argument")
    varname = None
    if len(bits) > 1:
        if bits[-2] == 'as':
            varname = bits[-1]
        bits = bits[:-2]
    return BBCodeNode(content, bits, varname)
