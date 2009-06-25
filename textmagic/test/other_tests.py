import unittest

from textmagic.test import TextMagicTestsBase
from textmagic.client import SendResponse
from textmagic.client import TextMagicError
from textmagic.gsm0338 import is_gsm

class ParameterErrorTests(TextMagicTestsBase):
    def testWrongCommandFails(self):
        try:
            self.client._execute_command({'cmd': 'nonexistent_command'}, SendResponse)
            self.fail('An error is expected to skip this line')
        except TextMagicError, e:
            self.assertEquals(e.error_code, 3)
            self.assertEquals(e.error_message, 'Command is undefined')

    def testInsufficientParametersFail(self):
        try:
            self.client._execute_command({'cmd': 'send'}, SendResponse)
            self.fail('An error is expected to skip this line')
        except TextMagicError, e:
            self.assertEquals(e.error_code, 4)
            self.assertEquals(e.error_message, 'Insufficient parameters')

class Gsm0338CharacterSetTests(unittest.TestCase):
    def testSomeStrings(self):
        self.assertEquals(is_gsm('Some latin text'), True)
        self.assertEquals(is_gsm(u'\uABCD'), False)
        self.assertEquals(is_gsm('{} \ ~ [ ] |'), True)  # Extended characters
        self.assertEquals(is_gsm(u'\u20AC'), True)  # Euro
        self.assertEquals(is_gsm(u'\u0041'), True)  # Latin capital A
        self.assertEquals(is_gsm(u'\u0391'), True)  # Greek capital Alpha
        self.assertEquals(is_gsm(u'\u0041\u0391'), True)  # A and Alpha
        self.assertEquals(is_gsm(u'\u2800\u2801\u2802\u2803 \u27F0'), False)
