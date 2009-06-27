import time

from textmagic.test import ONE_TEST_NUMBER
from textmagic.test import THREE_TEST_NUMBERS

from textmagic.test import TextMagicTestsBase
from textmagic.test import LiveUnsafeTests

class MessageStatusTestsBase(TextMagicTestsBase):
    def sendAndCheckStatusTo(self, numbers):
        message = 'sdfqwersdfgfdg'
        result = self.client.send(message, numbers)
        ids = result['message_id'].keys()
        self.getStatus(ids, message)
        return (ids, message)

    def getStatus(self, ids, message):
        result = self.client.message_status(ids)
        expected_keys = set(ids)
        self.assertEquals(set(result.keys()), expected_keys)
        statuses = []
        for id in ids:
            status = result[id]
            expected_keys = set(['status', 'text', 'reply_number', 'created_time'])
            if (len(status.keys()) == 4):
                pass
            elif (len(status.keys()) == 6):
                expected_keys.add('completed_time')
                expected_keys.add('credits_cost')
            else:
                self.fail("Unexpected number of return parameters: %s" % len(status.keys()))
            self.assertEquals(set(status.keys()), expected_keys)
            self.assertEquals(status['text'], message)
            self.assertEquals(status['reply_number'], '447624800500')
            self.assertTrue(isinstance(status['created_time'], time.struct_time))
            if (len(status.keys()) == 6):
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
