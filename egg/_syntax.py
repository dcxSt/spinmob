# based on https://github.com/art1415926535/PyQt5-syntax-highlighting
import spinmob
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import builtins

QRegExp = QtCore.QRegExp

QFont = QtGui.QFont
QColor = QtGui.QColor
QTextCharFormat = QtGui.QTextCharFormat
QSyntaxHighlighter = QtGui.QSyntaxHighlighter


def getQTextCharFormat(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


class LightThemeColors:

    Red = "#B71C1C"
    Pink = "#AA7777"
    Purple = "#4A148C"
    DeepPurple = "#311B92"
    Indigo = "#1A237E"
    Blue = "#0D47A1"
    LightBlue = "#01579B"
    Cyan = "#006064"
    Teal = "#004D40"
    Green = "#1B5E20"
    LightGreen = "#33691E"
    Lime = "#827717"
    Yellow = "#F57F17"
    Amber = "#FF6F00"
    Orange = "#E65100"
    DeepOrange = "#BF360C"
    Brown = "#3E2723"
    Grey = "#212121"
    BlueGrey = "#263238"


class DarkThemeColors:

    Red = "#FF7777"
    Pink = "#FFAAAA"
    Purple = "#CE93D8"
    DeepPurple = "#B39DDB"
    Indigo = "#9FA8DA"
    Blue = "#90CAF9"
    LightBlue = "#81D4FA"
    Cyan = "#80DEEA"
    Teal = "#80CBC4"
    Green = "#A5FFA7"
    LightGreen = "#C5E1A5"
    Lime = "#E6EE9C"
    Yellow = "#FFF59D"
    Amber = "#FFE082"
    Orange = "#FFCC80"
    DeepOrange = "#FFAB91"
    Brown = "#BCAAA4"
    Grey = "#EEEEEE"
    BlueGrey = "#B0BEC5"


LIGHT_STYLES = {
    'keyword': getQTextCharFormat(LightThemeColors.Blue, 'bold'),
    'builtin': getQTextCharFormat(LightThemeColors.Pink, 'bold'),
    'operator': getQTextCharFormat(LightThemeColors.Purple),
    'brace': getQTextCharFormat(LightThemeColors.Green),
    'defclass': getQTextCharFormat(LightThemeColors.Indigo, 'bold'),
    'string': getQTextCharFormat(LightThemeColors.Green, 'italic'),
    'string2': getQTextCharFormat(LightThemeColors.Green, 'italic'),
    'comment': getQTextCharFormat(LightThemeColors.Green, 'italic'),
    'self': getQTextCharFormat(LightThemeColors.Pink, 'bold, italic'),
    'numbers': getQTextCharFormat(LightThemeColors.Red),
}


DARK_STYLES = {
    'keyword' : getQTextCharFormat(DarkThemeColors.Blue, 'bold'),
    'builtin' : getQTextCharFormat(DarkThemeColors.Pink, 'bold'),
    'operator': getQTextCharFormat(DarkThemeColors.Red, 'bold'),
    'brace'   : getQTextCharFormat(DarkThemeColors.Purple),
    'defclass': getQTextCharFormat(DarkThemeColors.Indigo, 'bold'),
    'string'  : getQTextCharFormat(DarkThemeColors.Amber),
    'string2' : getQTextCharFormat(DarkThemeColors.DeepPurple),
    'comment' : getQTextCharFormat(DarkThemeColors.Green, 'italic'),
    'self'    : getQTextCharFormat(DarkThemeColors.Blue, 'bold'),
    'numbers' : getQTextCharFormat(DarkThemeColors.Teal),
}


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'as', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False', 'async', 'await',
    ]

    # Built-in
    builtin = dir(builtins)

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, 'string2')
        self.tri_double = (QRegExp('"""'), 2, 'string2')

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, 'keyword')
                  for w in PythonHighlighter.keywords]
        rules += [(r'\b%s\b' % w, 0, 'builtin')
                  for w in PythonHighlighter.builtin]
        rules += [(r'%s' % o, 0, 'operator')
                  for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, 'brace')
                  for b in PythonHighlighter.braces]

        # All other rules
        rules += [

            # 'self'
            (r'\bself\b', 0, 'self'),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, 'defclass'),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, 'defclass'),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, 'numbers'),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, 'numbers'),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, 'numbers'),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, 'string'),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, 'string'),

            # From '#' until a newline
            (r'#[^\n]*', 0, 'comment'),

        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def styles(self, style):
        return DARK_STYLES[style] if spinmob.settings['dark_theme_qt'] else LIGHT_STYLES[style]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            format = self.styles(format)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, self.styles(style))
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False

if __name__ == '__main__':
    import spinmob
    
    p = QtWidgets.QTextEdit()
    hl = PythonHighlighter(p.document())
    font = QtGui.QFont()
    font.setFamily("monospace")
    font.setFixedPitch(True)
    #font.setStyleHint(font.TypeWriter)
    p.setFont(font)
    l = spinmob.fun.read_lines('_syntax.py')
    p.setText(''.join(l))
    
    p.setGeometry(0,0, 1000, 800)
    p.show()
