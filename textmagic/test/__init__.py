"""
This module contains all the tests for the PyTextMagicSMS module.

All tests derive from TextMagicTestsBase.

The LiveUnsafeTests class is a "marker" for tests that cannot be run "live"
unchanged.

"""
import unittest
import time

from textmagic.test.mock_client import MockTextMagicClient

MAX_GSM0338_SMS_LENGTH = 160
MAX_GSM0338_MULTI_SMS_LENGTH = 153
A_GSM0338_CHARACTER = 'X'
MAX_UNICODE_SMS_LENGTH = 70
MAX_UNICODE_MULTI_SMS_LENGTH = 67
A_UNICODE_CHARACTER = '\u2800'

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
    """
    The base class for TextMagic tests.

    It contains the setUp method which instantiates a client for each test.

    """

    def setUp(self):
        self.client = client_class(api_username, api_password)
        self.client.logging = log_executed_commands

    def assertKeysEqualExpectedKeys(self, received_keys, expected_keys):
        self.assertEquals(set(received_keys), set(expected_keys))


class LiveUnsafeTests(object):
    """
    A test class must inherit from this class if its tests cannot run "live".

    If a test class derives from this class as well as TestMagicTestsBase
    it indicates that those tests cannot run "live" as they are. It might
    be simply impossible to run them "live" or they might be able to run "live"
    with some code changes.

    """

    pass
