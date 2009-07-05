import time

from textmagic.test import TextMagicTestsBase
from textmagic.test import LiveUnsafeTests


class ReceiveTestsBase(TextMagicTestsBase):

    def receiveMessages(self, id_in, more_expected=True, expected_text=None):
        result = self.client.receive(id_in)
        self.assertKeysEqualExpectedKeys(result, ['messages', 'unread'])
        self.assertEquals(result['unread'], 0)
        if not more_expected:
            self.assertEquals(len(result['messages']), 0)
            return
        message_ids = []
        for message in result['messages']:
            self.assertKeysEqualExpectedKeys(message,
                ['message_id', 'from', 'timestamp', 'text'])
            self.assertTrue(message['message_id'].isdigit())
            self.assertTrue(isinstance(message['from'], unicode))
            self.assertTrue(isinstance(message['text'], unicode))
            if expected_text:
                self.assertEquals(message['text'], expected_text)
            self.assertTrue(isinstance(message['timestamp'], time.struct_time))
            message_ids.append(message['message_id'])
        return message_ids


class LiveUnsafeReceiveTests(ReceiveTestsBase, LiveUnsafeTests):
    """
    Tests for the 'receive' command.
    
    These tests are live-unsafe because they assume certain messages in the
    inbox; as well as the number of messages returned in one system response.

    """

    def testReceiveLastTwoMessages(self):
        last_id, = self.receiveMessages(0, expected_text="Test reply....")
        last_id, = self.receiveMessages(last_id, expected_text="Second reply")
        self.receiveMessages(last_id, more_expected=False)

    def testReceiveFourMessagesInOne(self):
        self.assertTrue(len(self.receiveMessages(1)) == 4)

    def testReceiveUnicodeMessage(self):
        expected_text = u'\u2800\u2801\u2802\u2803 \u27f0'
        self.assertEquals(len(expected_text), 6)
        self.assertTrue(len(self.receiveMessages(2, expected_text=expected_text)) == 1)


class ReceiveTests(ReceiveTestsBase):
    """
    Live-safe tests for the 'receive' command.

    This test will succeed with any number (including zero) of messages in the
    inbox.

    """

    def testReceiveWhateverThereIs(self):
        self.receiveMessages(3)
