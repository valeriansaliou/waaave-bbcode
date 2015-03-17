from pygments.formatters import HtmlFormatter


class CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<div class="highlight"><pre>'
        for i, t in source:
            if i == 1:
                t = '<div class="code-line">%s</div>' % t
            yield i, t
        yield 0, '</pre></div>'