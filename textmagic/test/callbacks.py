import time

from textmagic.test import TextMagicTestsBase
from textmagic.client import StatusCallbackResponse
from textmagic.client import ReplyCallbackResponse
from textmagic.test import gmtime_from_localtime

class CallbackUrlTests(TextMagicTestsBase):

    def testStatusCallback(self):
        post_params = {
            'status' : "d",
            'message_id' : "8714718",
            'timestamp' : "1243797781",
            'credits_cost' : "1",
        }
        response = self.client.callbackMessage(post_params)
        self.assertTrue(isinstance(response, StatusCallbackResponse))
        self.assertTrue(isinstance(response['status'], unicode))
        self.assertEquals(response['status'], "d")
        self.assertTrue(isinstance(response['message_id'], unicode))
        self.assertEquals(response['message_id'], "8714718")
        self.assertTrue(isinstance(response['timestamp'], time.struct_time))
        self.assertEqual(
            gmtime_from_localtime(response['timestamp'])[:-1],
            (2009, 5, 31, 19, 23, 1, 6, 151))
        self.assertTrue(isinstance(response['credits_cost'], float))
        self.assertEquals(response['credits_cost'], 1)

    def testReceivedCallback(self):
        post_params = {
            'message_id' : "1788907",
            'text' : "Test Reply Message",
            'timestamp' : "1243837563",
            'from' : "27991114444",
        }
        response = self.client.callbackMessage(post_params)
        self.assertTrue(isinstance(response, ReplyCallbackResponse))
        self.assertTrue(isinstance(response['message_id'], unicode))
        self.assertEquals(response['message_id'], "1788907")
        self.assertTrue(isinstance(response['text'], unicode))
        self.assertEquals(response['text'], "Test Reply Message")
        self.assertTrue(isinstance(response['timestamp'], time.struct_time))
        self.assertEqual(
            gmtime_from_localtime(response['timestamp'])[:-1],
            (2009, 6, 1, 6, 26, 3, 0, 152))
        self.assertTrue(isinstance(response['from'], unicode))
        self.assertTrue(response['from'], "27991114444")

    def testReceivedCallbackWithUnicodeText(self):
        post_params = {
            'message_id' : "1788907",
            'text' : "\xE2\xA0\x80",
            'timestamp' : "1243837563",
            'from' : "27991114444",
        }
        response = self.client.callbackMessage(post_params)
        self.assertTrue(isinstance(response, ReplyCallbackResponse))
        self.assertEquals(response['text'], u'\u2800')
        self.assertEquals(len(response['text']), 1)
