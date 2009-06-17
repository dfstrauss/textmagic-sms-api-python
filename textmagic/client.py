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

    def logMessage(self, text):
        if self.logging:
            f = open('executed_commands.log', 'a')
            f.write("%s\n" % text)
            f.close()

    def callbackMessage(self, params_dict):
        """
        If you have a callback URL set up, you can pass the incoming POST
        parameters as a dictionary to this method to get a suitable
        response object.
        """
        if params_dict.has_key('status'):
            return StatusCallbackResponse(params_dict)
        else:
            return ReplyCallbackResponse(params_dict)

    def executeCommand(self, params_dict, responseClass):
        response = self._submitRequest(params_dict)
        self.logMessage("Response:     %s\n-----" % response)
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
        return self.executeCommand(params_dict, SendResponse)

    def send(self, text, phone, max_length=None):
        """
        Send a message to one or more numbers.
        text - The message
        phone - a list of phone numbers

        See http://api.textmagic.com/https-api/textmagic-api-commands#send
        (send_time parameter not implemented yet)
        """
        if is_gsm(text): unicode_ = 0
        else: unicode_ = 1
        return self._send(text, phone, max_length, unicode_)

    def account(self):
        """
        Get your account balance.
        """
        return self.executeCommand({
            'cmd': 'account'
        }, AccountResponse)

    def message_status(self, ids):
        """
        Get the delivery status of a sent message(s).
        """
        if not isinstance(ids, list): ids = [ids]
        return self.executeCommand({
            'cmd': 'message_status',
            'ids': ','.join([unicode(id) for id in ids])
        }, MessageStatusResponse)

    def receive(self, last_retrieved_id):
        """
        Receive reply SMS messages from your "inbox"
        """
        return self.executeCommand({
          'cmd': 'receive',
          'last_retrieved_id': unicode(last_retrieved_id)
        }, ReceiveResponse)

    def delete_reply(self, ids):
        """
        Delete a reply SMS from your "inbox"
        """
        if not isinstance(ids, list): ids = [ids]
        return self.executeCommand({
          'cmd': 'delete_reply',
          'ids': ','.join([unicode(id) for id in ids])
        }, DeleteReplyResponse)

class TextMagicClient(_TextMagicClientBase):
    """
    An instance of this class is used to perform API commands.
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
        self.logMessage("Parameters:   %s" % params)
        request = urllib2.Request(self.api_url, params)
        response = urllib2.urlopen(request)
        assert response.info()['Content-Type'] == 'application/json; charset=utf-8',\
            'Wrong HTTP Content-Type header!'
        return response.read()
