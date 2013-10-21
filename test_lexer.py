# encoding: utf-8

import unittest
import lexer

class LexerTest(unittest.TestCase):
    def doLex(self, input, expect):
        output = [(t.type, t.value) for t in lexer.run_lexer(input)]
        self.assertEqual(output, expect)

    def test_comment1(self):
        input = '~foo\nbar~baz\r\n'
        tokens = [('COMMENT', '~foo'),
                  ('NEWLINE', '\n'),
                  ('LITERAL', 'bar'),
                  ('COMMENT', '~baz'),
                  ('NEWLINE', '\r\n')]
        self.doLex(input, tokens)

    def test_comment2(self):
        input = '\\~foo\n\\\\~foo\n\\\\\\~foo\n'
        tokens = [('LITERAL', u'~'),
                  ('LITERAL', 'foo'),
                  ('NEWLINE', '\n'),
                  ('ESCAPE', u'\\'),
                  ('COMMENT', '~foo'),
                  ('NEWLINE', '\n'),
                  ('ESCAPE', u'\\'),
                  ('LITERAL', u'~'),
                  ('LITERAL', 'foo'),
                  ('NEWLINE', '\n')]
        self.doLex(input, tokens)

    def test_cdata1(self):
        input = '<<<>>> <<<>>> '
        tokens = [('OCDATA', '<<<'),
                  ('CCDATA', '>>>'),
                  ('SPACE', ' '),
                  ('OCDATA', '<<<'),
                  ('CCDATA', '>>>'),
                  ('SPACE', ' ')]
        self.doLex(input, tokens)

    def test_cdata2(self):
        input = '\\\\\\<<<>>> \\\\<<<>>> \\<<<>>> \\<<<<>>>'
        tokens = [('ESCAPE', '\\'),
                  ('LITERAL', '<<<'),
                  ('LITERAL', '>>>'),
                  ('SPACE', ' '),
                  ('ESCAPE', '\\'),
                  ('OCDATA', '<<<'),
                  ('CCDATA', '>>>'),
                  ('SPACE', ' '),
                  ('LITERAL', '<<<'),
                  ('LITERAL', '>>>'),
                  ('SPACE', ' '),
                  ('LITERAL', '\\<'),
                  ('OCDATA', '<<<'),
                  ('CCDATA', '>>>')]
        self.doLex(input, tokens)

    def test_cdata3(self):
        input = '<<< \\func[params]{arg} >>>'
        tokens = [('OCDATA', '<<<'),
                  ('CDATA', ' '),
                  ('CDATA', '\\'),
                  ('CDATA', 'func[params]{arg} '),
                  ('CCDATA', '>>>')]
        self.doLex(input, tokens)

    def test_cdata4(self):
        input = '<<< > >> >>>'
        tokens = [('OCDATA', '<<<'),
                  ('CDATA', ' '),
                  ('CDATA', '>'),
                  ('CDATA', ' '),
                  ('CDATA', '>>'),
                  ('CDATA', ' '),
                  ('CCDATA', '>>>')]
        self.doLex(input, tokens)

    def test_cdata5(self):
        input = '<<< \\\\ \\> \\>> \\>>> \\>>>>'
        tokens = [('OCDATA', '<<<'),
                  ('CDATA', ' '),
                  ('CDATA', '\\'),
                  ('CDATA', '\\'),
                  ('CDATA', ' '),
                  ('CDATA', '\\>'),
                  ('CDATA', ' '),
                  ('CDATA', '\\>>'),
                  ('CDATA', ' '),
                  ('CDATA', '>>>'),
                  ('CDATA', ' '),
                  ('CDATA', '\\>'),
                  ('CCDATA', '>>>')]
        self.doLex(input, tokens)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LexerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
