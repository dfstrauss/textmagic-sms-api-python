import unittest
import time

from textmagic.test.mock_client import MockTextMagicClient

MAX_GSM0338_SMS_LENGTH = 160
MAX_GSM0338_MULTI_SMS_LENGTH = 153
A_GSM0338_CHARACTER = 'X'
MAX_UNICODE_SMS_LENGTH = 70
MAX_UNICODE_MULTI_SMS_LENGTH = 67
A_UNICODE_CHARACTER = u'\u2800'

ONE_TEST_NUMBER = '9993334444'
THREE_TEST_NUMBERS = ['9993331234','9991239999','9991114444']

api_username = 'username'
api_password = 'password'
client_class = MockTextMagicClient
log_executed_commands=False
running_live=False

def gmtime_from_localtime(localtime):
    return time.gmtime(time.mktime(localtime))

class TextMagicTestsBase(unittest.TestCase):

    def setUp(self):
        self.client = client_class(api_username, api_password)
        self.client.logging = log_executed_commands
