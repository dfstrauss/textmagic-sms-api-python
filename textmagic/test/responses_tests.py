import time
import unittest

from textmagic import import_json
json = import_json()

import textmagic
from textmagic.test import gmtime_from_localtime

class TextMagicResponseTests(unittest.TestCase):
    def testSendResponse(self):
        message = json.loads('{"message_id":\
            {"8709767":"9993331234",\
            "8709768":"9991239999",\
            "8709769":"9991114444"},\
            "sent_text":"Test Message",\
            "parts_count":1}')
        response = textmagic.client.SendResponse(message)
        self.assertTrue(set(response.keys()) == set(['message_id', 'sent_text', 'parts_count']))
        self.assertTrue(isinstance(response['message_id'], dict))
        self.assertEquals(response['sent_text'], "Test Message")
        self.assertEquals(response['parts_count'], 1)
        self.assertEquals(set(response['message_id'].keys()), set(["8709767","8709768","8709769"]))
        self.assertEquals(response['message_id']['8709767'], "9993331234")
        self.assertEquals(response['message_id']['8709768'], "9991239999")
        self.assertEquals(response['message_id']['8709769'], "9991114444")

    def testErrorSendResponse(self):
        message = json.loads('{"message_id":[],"sent_text":null,"parts_count":1}')
        try:
            textmagic.client.SendResponse(message)
        except AssertionError, e:
            self.assertEquals(str(e), 'Invalid server response - message_id cannot be empty!')

    def testAccountResponse(self):
        message = json.loads('{"balance":"96.5"}')
        response = textmagic.client.AccountResponse(message)
        self.assertEquals(response['balance'], 96.5)
        self.assertTrue(response.keys() == ['balance'])

    def testReceiveResponse(self):
        message = json.loads('{"messages":\
            [{"message_id":"1787519",\
            "from":"27829991111",\
            "timestamp":1243629516,\
            "text":"Test reply...."},\
            {"message_id":"1787603",\
            "from":"27829991111",\
            "timestamp":1243635007,\
            "text":"\u2800\u2801\u2802\u2803 \u27f0"}],\
            "unread":0}')
        response = textmagic.client.ReceiveResponse(message)
        self.assertTrue(set(response.keys()) == set(['messages', 'unread']))
        self.assertTrue(len(response['messages']) == 2)
        self.assertEquals(response['unread'], 0)
        self.assertTrue(isinstance(response['messages'], list))
        self.assertTrue(isinstance(response['messages'][0], dict))
        self.assertTrue(isinstance(response['messages'][1], dict))
        self.assertEquals(response['messages'][0]['message_id'], '1787519')
        self.assertEquals(response['messages'][0]['from'], '27829991111')
        self.assertEquals(
            gmtime_from_localtime(response['messages'][0]['timestamp']),
            (2009, 5, 29, 20, 38, 36, 4, 149, 0))
        self.assertEquals(response['messages'][0]['text'], 'Test reply....')
        self.assertEquals(response['messages'][1]['message_id'], '1787603')
        self.assertEquals(response['messages'][1]['from'], '27829991111')
        self.assertEquals(
            gmtime_from_localtime(response['messages'][1]['timestamp']),
            (2009, 5, 29, 22, 10, 7, 4, 149, 0))
        self.assertEquals(response['messages'][1]['text'], u'\u2800\u2801\u2802\u2803 \u27f0')

    def assertMessageStatusBaseParameters(self, response):
        self.assertTrue(len(response) == 1)
        self.assertTrue(response.keys()[0].isdigit())
        status = response[response.keys()[0]]
        self.assertTrue(isinstance(status, dict))
        self.assertTrue(isinstance(status['text'], unicode))
        self.assertTrue(isinstance(status['status'], unicode))
        self.assertEquals(len(status['status']), 1)
        self.assertTrue(isinstance(status['created_time'], time.struct_time))
        self.assertTrue(isinstance(status['reply_number'], unicode))
        self.assertTrue(status['reply_number'].isdigit())
        return status

    def testMessageStatusInProcessResponse(self):
        message = json.loads('{"8768531":\
            {"text":"sdfqwersdfgfdg",\
            "status":"a",\
            "created_time":"1244401369",\
            "reply_number":"447624800500"}}')
        response = textmagic.client.MessageStatusResponse(message)
        self.assertTrue(response.keys() == ['8768531'])
        self.assertMessageStatusBaseParameters(response)

    def testMessageStatusDoneResponse(self):
        message = json.loads('{"8768531":\
            {"text":"sdfqwersdfgfdg",\
            "status":"d",\
            "created_time":"1244401369",\
            "reply_number":"447624800500",\
            "completed_time":"1244401465",\
            "credits_cost":"0.5"}}')
        response = textmagic.client.MessageStatusResponse(message)
        self.assertTrue(response.keys() == ['8768531'])
        status = self.assertMessageStatusBaseParameters(response)
        self.assertTrue(isinstance(status['completed_time'], time.struct_time))
        self.assertTrue(isinstance(status['credits_cost'], float))

    def testMessageStatusDoneResponseNullTime(self):
        message = json.loads('{"8768531":\
            {"text":"sdfqwersdfgfdg",\
            "status":"d",\
            "created_time":"1244401369",\
            "reply_number":"447624800500",\
            "completed_time":null,\
            "credits_cost":"0.5"}}')
        response = textmagic.client.MessageStatusResponse(message)
        status = self.assertMessageStatusBaseParameters(response)
        self.assertEquals(status['completed_time'], None)
        self.assertTrue(isinstance(status['credits_cost'], float))

    def testDeleteReplyResponse(self):
        message = json.loads('{"deleted":["1787548","1787572"]}')
        response = textmagic.client.DeleteReplyResponse(message)
        self.assertTrue(response.keys() == ['deleted'])
        self.assertTrue(isinstance(response['deleted'], list))
        for message_id in response['deleted']:
            self.assertTrue(message_id.isdigit())

    def testCheckNumberResponse(self):
        message = json.loads('{\
            "27123456789":{"price":0.5,"country":"ZA"},\
            "44123456789":{"price":1,"country":"GB"}}')
        response = textmagic.client.CheckNumberResponse(message)
        self.assertTrue(set(response.keys()) == set(['27123456789', '44123456789']))
        for number in response.iterkeys():
            self.assertTrue(isinstance(response[number]['price'], float))
            self.assertEquals(len(response[number]['country']), 2)
            self.assertTrue(isinstance(response[number]['country'], unicode))

    def testErrorResponse(self):
        message = json.loads('{"error_code":15,"error_message":"Unicode symbols detected"}')
        response = textmagic.client.TextMagicError(message)
        self.assertTrue(isinstance(response, Exception))
        self.assertTrue(isinstance(response.error_code, int))
        self.assertTrue(isinstance(response.error_message, unicode))

