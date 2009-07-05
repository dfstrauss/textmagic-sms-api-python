"""
This file implements the response messages returned from TextMagic API calls.

Each response class is named after its API call:
 - SendResponse
 - AccountResponse
 - ReceiveResponse
 - MessageStatusResponse
 - DeleteReplyResponse
 - CheckNumberResponse

The two types of notification messages are:
 - StatusCallbackResponse
 - ReplyCallbackResponse

There is also an Exception (TextMagicError) which is raised when an API
error occurs.

"""

import time

def _cast_to_type(type, value):
    if value is None:
        return None
    return type(value)

def _time_or_none(value):
    if value is None:
        return None
    return time.localtime(float(value))


class TextMagicError(Exception):
    """
    This is the exception raised when the TextMagic system returns an error.

    See error codes at http://api.textmagic.com/https-api/api-error-codes

    """

    def __init__(self, dict_):
        self.error_code = _cast_to_type(int, dict_['error_code'])
        self.error_message = _cast_to_type(unicode, dict_['error_message'])

    def __str__(self):
        return "[Error %d] %s" % (self.error_code, self.error_message)


class SendResponse(dict):

    def __init__(self, dict_):
        super(SendResponse, self).__init__(dict_)
        self['sent_text'] = _cast_to_type(unicode, self['sent_text'])
        self['parts_count'] = _cast_to_type(int, self['parts_count'])
        assert len(self['message_id']), 'Invalid server response - message_id cannot be empty!'
        for key in self['message_id']:
            self['message_id'][key] = _cast_to_type(unicode, self['message_id'][key])


class AccountResponse(dict):

    def __init__(self, dict_):
        super(AccountResponse, self).__init__(dict_)
        self['balance'] = _cast_to_type(float, self['balance'])


class ReceiveResponse(dict):

    def __init__(self, dict_):
        super(ReceiveResponse, self).__init__(dict_)
        self['unread'] = _cast_to_type(int, self['unread'])
        for message in self['messages']:
            message['message_id'] = _cast_to_type(unicode, message['message_id'])
            message['from'] = _cast_to_type(unicode, message['from'])
            message['text'] = _cast_to_type(unicode, message['text'])
            message['timestamp'] = _time_or_none(message['timestamp'])


class MessageStatusResponse(dict):

    def __init__(self, dict_):
        super(MessageStatusResponse, self).__init__(dict_)
        for key in self:
            self[key]['text'] = _cast_to_type(unicode, self[key]['text'])
            self[key]['status'] = _cast_to_type(unicode, self[key]['status'])
            self[key]['created_time'] = _time_or_none(self[key]['created_time'])
            self[key]['reply_number'] = _cast_to_type(unicode, self[key]['reply_number'])
            if 'completed_time' in self[key]:
                self[key]['completed_time'] = _time_or_none(self[key]['completed_time'])
                self[key]['credits_cost'] = _cast_to_type(float, self[key]['credits_cost'])


class DeleteReplyResponse(dict):

    def __init__(self, dict_):
        super(DeleteReplyResponse, self).__init__(dict_)
        for idx in xrange(len(self['deleted'])):
            self['deleted'][idx] = _cast_to_type(unicode, self['deleted'][idx])


class CheckNumberResponse(dict):

    def __init__(self, dict_):
        super(CheckNumberResponse, self).__init__(dict_)
        for key in self:
            self[key]['price'] = _cast_to_type(float, self[key]['price'])
            self[key]['country'] = _cast_to_type(unicode, self[key]['country'])


class StatusCallbackResponse(dict):

    def __init__(self, dict_):
        super(StatusCallbackResponse, self).__init__(dict_)
        self['status'] = _cast_to_type(unicode, self['status'])
        self['message_id'] = _cast_to_type(unicode, self['message_id'])
        self['timestamp'] = _time_or_none(self['timestamp'])
        self['credits_cost'] = _cast_to_type(float, self['credits_cost'])


class ReplyCallbackResponse(dict):

    def __init__(self, dict_):
        super(ReplyCallbackResponse, self).__init__(dict_)
        self['message_id'] = _cast_to_type(unicode, self['message_id'])
        self['text'] = _cast_to_type(unicode, self['text'].decode('utf-8'))
        self['timestamp'] = _time_or_none(self['timestamp'])
        self['from'] = _cast_to_type(unicode, self['from'])
