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
    'LITERAL',
    'CDATA',
    'LCDATA',
    'RCDATA',
    'PERCENT',
)

states = (
    ('cdata', 'exclusive'),
)

def t_ESCAPE(t):
    r'\\'
    return t

def t_NEWLINE(t):
    r'\r?\n'
    return t

def t_SPACE(t):
    r'[ \t]+'
    return t

def t_COMMENT(t):
    r'^~[^\n]*|(?<=[^\\])~[^\n]*'
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

def t_LCDATA(t):
    r'(?<=[^\\])%%%'
    t.lexer.push_state('cdata')
    return t

def t_LITERAL(t):
    r'[^\s\\\{\}\[\]~]+'
    return t

def t_error(t):
    print u"Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def t_cdata_ESCAPE(t):
    r'\\'
    return t

def t_cdata_PERCENT(t):
    r'(?<=\\)%|(?<=[^\\])%{1,2}(?!%)'
    return t

def t_cdata_RCDATA(t):
    r'(?<=[^\\])%%%'
    t.lexer.pop_state()
    return t

def t_cdata_CDATA(t):
    r'[^\\%]+'
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
