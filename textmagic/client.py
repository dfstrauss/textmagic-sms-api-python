import urllib
import urllib2

from textmagic.responses import SendResponse
from textmagic.responses import AccountResponse
from textmagic.responses import ReceiveResponse
from textmagic.responses import MessageStatusResponse
from textmagic.responses import DeleteReplyResponse
from textmagic.responses import StatusCallbackResponse
from textmagic.responses import ReplyCallbackResponse
from textmagic.responses import TextMagicError

from textmagic.gsm0338 import is_gsm

from textmagic import import_json
json = import_json()

class _TextMagicClientBase(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logging = False

    def _log_message(self, text):
        if self.logging:
            f = open('executed_commands.log', 'a')
            f.write("%s\n" % text)
            f.close()

    def callbackMessage(self, params_dict):
        """
        Interpret a notification sent to your callback URL.

        If you have a callback URL set up, you can pass the incoming POST
        parameters as a dictionary to this method to get a suitable
        response object.

        If the response object is a textmagic.responses.StatusCallbackResponse
        it is a message delivery notification with:
            response['status'] is the delivery status as described at
                http://api.textmagic.com/https-api/sms-delivery-notification-codes
            response['message_id'] is the message id being reported on
            response['timestamp'] is the timestamp of the status being reported
                as a time.struct_time in local time
            response['credits_cost'] is the number of credits used by this
                message

        If the response object is a textmagic.responses.ReplyCallbackResponse
        it is a reply message notification with:
            response['message_id'] is the id of the message in your Inbox
            response['text'] is the text of the received message
            response['timestamp'] is the delivery time as a time.struct_time
                 in local time
            response['from'] is the phone number from which the reply was sent

        """
        if params_dict.has_key('status'):
            return StatusCallbackResponse(params_dict)
        else:
            return ReplyCallbackResponse(params_dict)

    def _executeCommand(self, params_dict, responseClass):
        response = self._submitRequest(params_dict)
        self._log_message("Response:     %s\n-----" % response)
        resp = json.loads(response)
        if resp.has_key('error_code'):
            raise TextMagicError(resp)
        else:
            return responseClass(resp)

    def _send(self, text, phone, max_length, unicode_):
        if not isinstance(phone, list): phone = [phone]
        if unicode_ is None:
            if is_gsm(text): unicode_ = 0
            else: unicode_ = 1
        params_dict = {
          'cmd': 'send',
          'text': text.encode('utf-8'),
          'phone': str(','.join([unicode(number) for number in phone])),
          'unicode': str(unicode_),
          }
        if max_length is not None:
            params_dict['max_length'] = str(max_length)
        return self._executeCommand(params_dict, SendResponse)

    def send(self, text, phone, max_length=None):
        """
        Send a message to one or more numbers.

        If the message is too long for a single SMS it will be split up into
        a maximum of three separate messages. Maximum SMS length is usually
        160 characters (unless the message contains Unicode characters in
        which case the maximum length is 70 characters). With the max_length
        parameter you can control how many parts a message is broken into.

        Parameters:
            text - the message
            phone - one phone number or a list of numbers
            max_length - maximum number of parts to split the message into

        Return:
            A textmagic.responses.SendResponse

            response['message_id'] is a dict where the keys are message ids
                (as allocated by the TextMagic system) and the values are
                the corresponding destination phone numbers
            response['sent_text'] is the text that was sent
            response['parts_count'] is the number of parts the message was
                split into
        """
        if is_gsm(text): unicode_ = 0
        else: unicode_ = 1
        return self._send(text, phone, max_length, unicode_)

    def account(self):
        """
        Get your account balance.

        Parameters:
            None

        Return:
            A textmagic.responses.AccountResponse

            response['balance'] is the number of credits in your account
        """
        return self._executeCommand({
            'cmd': 'account'
        }, AccountResponse)

    def message_status(self, ids):
        """
        Get the delivery status of one or more sent messages.

        Parameters:
            ids - one message id or a list of message ids

        Return:
            A textmagic.responses.MessageStatusResponse

            response[id] is a dict:
                message['text'] is the message text
                message['status'] is the delivery status as described at
                    http://api.textmagic.com/https-api/sms-delivery-notification-codes
                message['created_time'] is the time the message was created as
                    a time.struct_time in local time
                message['reply_number'] is the phone number to which replies
                    can be sent
                message['credits_cost'] (optional) is the number of credits
                    used to send the message
                message['completed_time'] (optional) is the time the message
                    completed as a time.struct_time in local time
            response['unread'] is the number of unread messages in your Inbox
        """
        if not isinstance(ids, list): ids = [ids]
        return self._executeCommand({
            'cmd': 'message_status',
            'ids': ','.join([unicode(id) for id in ids])
        }, MessageStatusResponse)

    def receive(self, last_retrieved_id):
        """
        Receive reply SMS messages from your TextMagic Inbox.

        Parameters:
            last_retrieved_id - the message id of the last message retrieved

        Return:
            A textmagic.responses.ReceiveResponse

            response['messages'] is a list of dicts:
                message['message_id'] is the message id
                message['from'] is the source phone number
                message['timestamp'] is the time the message was received as
                    a time.struct_time in local time
                message['text'] is the text of the message
            response['unread'] is the number of unread messages in your Inbox
        """
        return self._executeCommand({
          'cmd': 'receive',
          'last_retrieved_id': unicode(last_retrieved_id)
        }, ReceiveResponse)

    def delete_reply(self, ids):
        """
        Delete one or more reply SMS messages from your TextMagic Inbox.

        Parameters:
            ids - one message id or a list of message ids

        Return:
            A textmagic.responses.DeleteReplyResponse

            response['deleted'] is a list of message ids actually deleted
        """
        if not isinstance(ids, list): ids = [ids]
        return self._executeCommand({
          'cmd': 'delete_reply',
          'ids': ','.join([unicode(id) for id in ids])
        }, DeleteReplyResponse)

class TextMagicClient(_TextMagicClientBase):
    """
    An instance of this class is used to perform API commands.

    An instance of this class has to be created to make TextMagic SMS API
    calls. Once the instance is created, you can invoke the TextMagic API
    functionality by calling:
        - send
        - account
        - message_status
        - receive
        - delete_reply
    And you can interpret callback notifications by calling:
        - callbackMessage
    """

    api_url = 'https://www.textmagic.com/app/api'

    def __init__(self, username, password):
        """
        Username and password must be provided to instantiate a client.
        """
        super(TextMagicClient, self).__init__(username, password)

    def _submitRequest(self, params_dict):
        params_dict['username'] = self.username
        params_dict['password'] = self.password
        params = urllib.urlencode(params_dict)
        self._log_message("Parameters:   %s" % params)
        request = urllib2.Request(self.api_url, params)
        response = urllib2.urlopen(request)
        assert response.info()['Content-Type'] == 'application/json; charset=utf-8',\
            'Wrong HTTP Content-Type header!'
        return response.read()