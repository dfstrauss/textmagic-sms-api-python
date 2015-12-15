import time

from textmagic.test import ONE_TEST_NUMBER
from textmagic.test import THREE_TEST_NUMBERS

from textmagic.test import TextMagicTestsBase
from textmagic.test import LiveUnsafeTests


class MessageStatusTestsBase(TextMagicTestsBase):

    def sendAndCheckStatusTo(self, numbers):
        message = 'sdfqwersdfgfdg'
        response = self.client.send(message, numbers)
        ids = list(response['message_id'].keys())
        self.getStatus(ids, message)
        return (ids, message)

    def getStatus(self, ids, message):
        response = self.client.message_status(ids)
        self.assertKeysEqualExpectedKeys(response, ids)
        statuses = []
        for id in ids:
            status = response[id]
            expected_keys = ['status', 'text', 'reply_number', 'created_time']
            if (len(status) == 4):
                pass
            elif (len(status) == 6):
                expected_keys.append('completed_time')
                expected_keys.append('credits_cost')
            else:
                self.fail("Unexpected number of return parameters: %s" % len(status))
            self.assertKeysEqualExpectedKeys(status, expected_keys)
            self.assertEquals(status['text'], message)
            self.assertEquals(status['reply_number'], '447624800500')
            self.assertTrue(isinstance(status['created_time'], time.struct_time))
            if (len(status) == 6):
                self.assertTrue(isinstance(status['completed_time'], time.struct_time))
                self.assertTrue(isinstance(status['credits_cost'], float))
            statuses.append(status['status'])
        return statuses


class MessageStatusTests(MessageStatusTestsBase):

    def testMessageStatusWhenSendingOneMessage(self):
        self.sendAndCheckStatusTo(ONE_TEST_NUMBER)

    def testMessageStatusWhenSendingThreeMessages(self):
        self.sendAndCheckStatusTo(THREE_TEST_NUMBERS)


class LiveUnsafeMessageStatusTests(MessageStatusTestsBase, LiveUnsafeTests):
    """
    This test is live-unsafe because it is intended to be sent to a real
    telephone number. It keeps asking for message status until it receives
    a "delivered" response.

    """

    def testMessageStatusWhenPhoneIsSwitchedOff(self):
        ids, message = self.sendAndCheckStatusTo(['27991114444'])
        while True:
            s, = self.getStatus(ids, message)
            if (s == 'd'):
                break
