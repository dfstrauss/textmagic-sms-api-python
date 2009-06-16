import time

from textmagic.test import ONE_TEST_NUMBER
from textmagic.test import THREE_TEST_NUMBERS

from textmagic.test import TextMagicTestsBase

class MessageStatusTests(TextMagicTestsBase):
    def sendAndCheckStatusTo(self, numbers):
        message = 'sdfqwersdfgfdg'
        result = self.client.send(message, numbers, 0)
        ids = result['message_id'].keys()
        statuses = self.getStatus(ids, message)
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

    def testMessageStatusWhenSendingOneMessage(self):
        self.sendAndCheckStatusTo(ONE_TEST_NUMBER)
    def testMessageStatusWhenSendingThreeMessages(self):
        self.sendAndCheckStatusTo(THREE_TEST_NUMBERS)

    def testMessageStatusWhenPhoneIsSwitchedOff(self):
        ids, message = self.sendAndCheckStatusTo(['27991114444'])
        while True:
            s, = self.getStatus(ids, message)
            if (s == 'd'):
                break
