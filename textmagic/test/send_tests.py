import time

import textmagic

from textmagic.test import ONE_TEST_NUMBER
from textmagic.test import THREE_TEST_NUMBERS

from textmagic.test import MAX_GSM0338_SMS_LENGTH
from textmagic.test import MAX_GSM0338_MULTI_SMS_LENGTH
from textmagic.test import A_GSM0338_CHARACTER
from textmagic.test import MAX_UNICODE_SMS_LENGTH
from textmagic.test import MAX_UNICODE_MULTI_SMS_LENGTH
from textmagic.test import A_UNICODE_CHARACTER

from textmagic.test import TextMagicTestsBase
from textmagic.test import LiveUnsafeTests

from textmagic.client import TextMagicError


class SendTestsBase(TextMagicTestsBase):
    """
    Abstract class implementing a generic succeeding and failing "send" test
    case.

    """

    expected_keys = ['sent_text', 'message_id', 'parts_count']

    def succeedingSendCase(self, message, numbers, expected_parts,
                            max_length=None, send_time=None, unicode=None, sender=None):
        response = self.client._send(message, numbers, max_length, send_time, unicode, sender)
        if not isinstance(numbers, list):
            numbers=[numbers]
        expected_keys = list(self.expected_keys)
        if sender is not None:
            expected_keys.extend(['from'])
        self.assertKeysEqualExpectedKeys(response, expected_keys)
        self.assertEquals(response['sent_text'], message)
        self.assertEquals(len(response['message_id']), len(numbers))
        self.assertEquals(set(response['message_id'].values()), set(numbers))
        for message_id in response['message_id']:
            self.assertTrue(message_id.isdigit())
        self.assertEquals(response['parts_count'], expected_parts)

    def failingSendCase(self, message, numbers, error_code, error_message,
                        max_length=None, send_time=None, unicode=None, sender=None):
        try:
            self.client._send(message, numbers, max_length, send_time, unicode, sender)
            self.fail('An error is expected to skip this line')
        except TextMagicError, e:
            self.assertEquals(e.error_code, error_code)
            self.assertEquals(e.error_message, error_message)


class BasicSendTests(SendTestsBase):
    """
    Test the very basics.

    """

    def testOneShortMessageSucceeds(self):
        self.succeedingSendCase(
            message='Test Message',
            numbers=ONE_TEST_NUMBER,
            expected_parts=1)

    def testThreeShortMessagesSucceed(self):
        self.succeedingSendCase(
            message='Test Message',
            numbers=THREE_TEST_NUMBERS,
            expected_parts=1)

    def testOneShortUnicodeMessageSucceeds(self):
        self.succeedingSendCase(
            message=u'\u2800\u2801\u2802\u2803 \u27F0',
            numbers=ONE_TEST_NUMBER,
            expected_parts=1)

    def testSendCanBeCalledWithoutOptionalParametersGsm0338(self):
        message = 'Test Message'
        number = ONE_TEST_NUMBER
        response = self.client.send(message, number)
        self.assertKeysEqualExpectedKeys(response, self.expected_keys)
        self.assertEquals(response['sent_text'], message)
        self.assertEquals(len(response['message_id']), 1)

    def testSendCanBeCalledWithoutOptionalParametersUnicode(self):
        message = u'\u2800\u2801\u2802\u2803 \u27F0'
        number = ONE_TEST_NUMBER
        response = self.client.send(message, number)
        self.assertKeysEqualExpectedKeys(response, self.expected_keys)
        self.assertEquals(response['sent_text'], message)
        self.assertEquals(len(response['message_id']), 1)


class LiveUnsafeBasicSendTests(BasicSendTests, LiveUnsafeTests):
    """
    Test the very basics - but needing server-setup to work

    """

    def testOneShortMessageWithSenderSucceeds(self):
        self.succeedingSendCase(
                message='Test Message',
                numbers=ONE_TEST_NUMBER,
                expected_parts=1,
                sender='xyz')


class MultipartSendTests(SendTestsBase):
    """
    Abstract class to test message lengths.
    
    This class must be extended to test different character sets

    """

    def succeedingSendLengthCase(self, length, expected_parts):
        self.succeedingSendCase(
            message=self.char*length,
            numbers=ONE_TEST_NUMBER,
            expected_parts=expected_parts)

    def testLongestOnePartMessageSucceeds(self):
        self.succeedingSendLengthCase(self.max_sms_length, 1)

    def testShortestTwoPartMessageSucceeds(self):
        self.succeedingSendLengthCase(self.max_sms_length+1, 2)

    def testLongestTwoPartMessageSucceeds(self):
        self.succeedingSendLengthCase(self.max_multi_sms_length*2, 2)

    def testShortestThreePartMessageSucceeds(self):
        self.succeedingSendLengthCase((self.max_multi_sms_length*2)+1, 3)

    def testLongestThreePartMessageSucceeds(self):
        self.succeedingSendLengthCase(self.max_multi_sms_length*3, 3)


class MultipartGsm0338SendTests(MultipartSendTests):

    max_sms_length = MAX_GSM0338_SMS_LENGTH
    max_multi_sms_length = MAX_GSM0338_MULTI_SMS_LENGTH
    char = A_GSM0338_CHARACTER


class MultipartUnicodeSendTests(MultipartSendTests):

    max_sms_length = MAX_UNICODE_SMS_LENGTH
    max_multi_sms_length = MAX_UNICODE_MULTI_SMS_LENGTH
    char = A_UNICODE_CHARACTER


class MaxLengthSendTests(SendTestsBase):

    def testTooLongMessageErrorWhenMaxLengthIsOne(self):
        self.failingSendCase(
            message=A_GSM0338_CHARACTER*MAX_GSM0338_MULTI_SMS_LENGTH*2,
            numbers=ONE_TEST_NUMBER,
            error_code=7,
            error_message='Too long message',
            max_length = 1)

    def testTooLongMessageErrorWhenMaxLengthIsTwo(self):
        self.failingSendCase(
            message=A_GSM0338_CHARACTER*MAX_GSM0338_MULTI_SMS_LENGTH*3,
            numbers=ONE_TEST_NUMBER,
            error_code=7,
            error_message='Too long message',
            max_length = 2)

    def testOnePartMessageFailsWhenMaxLengthIsZero(self):
        self.failingSendCase(
            message=A_GSM0338_CHARACTER*MAX_GSM0338_SMS_LENGTH,
            numbers=ONE_TEST_NUMBER,
            max_length = 0,
            error_code=10,
            error_message='Wrong parameter value 0 for parameter max_length')

    def testTwoPartMessageFailsWhenMaxLengthIsZero(self):
        self.failingSendCase(
            message=A_GSM0338_CHARACTER*MAX_GSM0338_MULTI_SMS_LENGTH*2,
            numbers=ONE_TEST_NUMBER,
            max_length = 0,
            error_code=10,
            error_message='Wrong parameter value 0 for parameter max_length')

    def testThreePartMessageSucceedsWhenMaxLengthIsUnspecified(self):
        self.succeedingSendCase(
            message=A_GSM0338_CHARACTER*MAX_GSM0338_MULTI_SMS_LENGTH*3,
            numbers=ONE_TEST_NUMBER,
            expected_parts=3)


class SendCharacterSetsTests(SendTestsBase):

    def testEscapedCharactersLengthenMessage(self):
        escaped_chars = '{}\~[]|'
        for escaped_char in escaped_chars:
            message='a'*(MAX_GSM0338_SMS_LENGTH-1)+escaped_char
            self.assertEquals(len(message), MAX_GSM0338_SMS_LENGTH)
            self.succeedingSendCase(
                message=message,
                numbers=ONE_TEST_NUMBER,
                expected_parts=2)


class SendTimeTests(SendTestsBase):

    def _time_now(self):
        if textmagic.test.running_live:
            return time.time()
        else:
            return 1245879223

    def _sendTimeInFutureSucceeds(self, send_time):
        message = 'Message from the future'
        self.succeedingSendCase(
            message=message,
            numbers=ONE_TEST_NUMBER,
            expected_parts=1,
            send_time=send_time)

    def testSendTimeAsStructTimeInFutureSucceeds(self):
        self._sendTimeInFutureSucceeds(time.localtime(self._time_now()+120))

    def testSendTimeAsStructTimeInPastSucceeds(self):
        self._sendTimeInFutureSucceeds(time.localtime(self._time_now()-300))

    def testSendTimeAsUnixTimeInFutureSucceeds(self):
        self._sendTimeInFutureSucceeds(self._time_now()+120)

    def testSendTimeAsUnixTimeInPastSucceeds(self):
        self._sendTimeInFutureSucceeds(self._time_now()-300)


class SendErrorsTests(SendTestsBase):
    """
    Test error messages on sending.

    """

    def testEmptyMessageFails(self):
        self.failingSendCase(
            message='',
            numbers=ONE_TEST_NUMBER,
            error_code=1,
            error_message='Messages text is empty')

    def testWrongPhoneNumberFormatFails(self):
        self.failingSendCase(
            message='Error testing message',
            numbers=['1234'],
            error_code=9,
            error_message='Wrong phone number format')

    def testWrongPasswordFails(self):
        self.client = textmagic.test.client_class(self.client.username, 'koos')
        self.failingSendCase(
            message='Wrong password testing message',
            numbers=ONE_TEST_NUMBER,
            error_code=5,
            error_message='Invalid username & password combination')

    def testWrongValueForUnicodeParameterFails(self):
        self.failingSendCase(
            message='Error testing message',
            numbers=ONE_TEST_NUMBER,
            unicode=10,
            error_code=10,
            error_message='Wrong parameter value 10 for parameter unicode')

    def testUnicodeMessageThatSaysNotUnicodeReportsTooLongUnicodeMessageReturnsError(self):
        self.failingSendCase(
            message=u'\uABCD'*(MAX_GSM0338_MULTI_SMS_LENGTH),
            numbers=ONE_TEST_NUMBER,
            unicode=0,
            error_code=15,
            error_message='Unicode symbols detected')

    def testGsm0338MessageThatSaysUnicodeSentAsGsm0338(self):
        self.succeedingSendCase(
            message='x'*(MAX_UNICODE_SMS_LENGTH*3),
            numbers=ONE_TEST_NUMBER,
            unicode=1,
            expected_parts=2)
