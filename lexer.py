# encoding: utf-8

import re
import ply.lex as lex

tokens = (
    'ESCAPE',
    'NEWLINE',
    'SPACE',
    'COMMENT',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'FUNCTION',
    'VARIABLE',
    'LITERAL',
    'CDATA',
    'OCDATA',  # open CDATA mark (<<<)
    'CCDATA',  # close CDATA mark (>>>)
)

states = (
    ('cdata', 'exclusive'),
)

def t_ESCAPE(t):
    r'\\\\'
    t.value = u'\\'
    return t

def t_NEWLINE(t):
    r'\r?\n'
    return t

def t_SPACE(t):
    r'[ \t]+'
    return t

def t_COMMENT(t):
    r'~[^\r\n]*'
    return t

def t_LBRACE(t):
    r'(?<=[^\\])\{'
    return t

def t_RBRACE(t):
    r'(?<=[^\\])\}'
    return t

def t_LBRACKET(t):
    r'(?<=[^\\])\['
    return t

def t_RBRACKET(t):
    r'(?<=[^\\])\]'
    return t

def t_OCDATA(t):
    r'<<<'
    t.lexer.push_state('cdata')
    return t

def t_FUNCTION(t):
    r'(?<=\\)[_A-Za-z][_0-9A-Za-z]*'
    return t

def t_VARIABLE(t):
    r'\$[_A-Za-z][_0-9A-Za-z]*'
    return t

def t_LITERAL(t):
    r'[^\s\\\{\}\[\]\$~]+|\\<{1,3}(?!<)|\\<(?=<<<)|\\~|(?<=\\)\{|(?<=\\)\}|(?<=\\)\[|(?<=\\)\]'
    if t.value == u'\\<<<':
        t.value = u'<<<'
    elif t.value == u'\\~':
        t.value = u'~'
    return t

def t_error(t):
    print u"Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def t_cdata_CCDATA(t):
    r'(?<=[^\\])>>>'
    t.lexer.pop_state()
    return t

def t_cdata_CDATA(t):
    r'[^>\\]+|\\>{,3}(?!>)|\\>(?=>>>)|(?<=[^\\])>{1,2}(?!>)'
    if t.value == u'\\>>>':
        t.value = u'>>>'
    return t

def t_cdata_error(t):
    print u"Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def build_lexer():
    return lex.lex(reflags=re.UNICODE)

def run_lexer(data):
    lexer = build_lexer()
    lexer.input(data)
    return list(lexer)

data = u"""
~ 这是注释
  Hello, $name!
\\ruby[まほう]{魔法} ~this is also a comment
<<< \\ > >> \\> \\>> \\>>> \\>>>>
<<< > >> \\\\ \\> \\>> \\>>> \\>>>>
"""

def _test():
    print data
    tokens = run_lexer(data)
    for tok in tokens:
        if isinstance(tok.value, unicode):
            tok_str = "'" + tok.value.encode('utf-8') + "'"
            tok_str = tok_str.replace('\\', '\\\\').replace('\n', '\\n')
        else:
            tok_str = str(tok.value)
        print '%s.%-4s %-10s %s' % (tok.lineno, tok.lexpos, tok.type, tok_str)

if __name__ == '__main__':
    _test()
