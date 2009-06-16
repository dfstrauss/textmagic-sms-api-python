import time

def cast_to_type(type, value):
    if value is None: return None
    return type(value)

def time_or_none(value):
    if value is None: return None
    return time.localtime(float(value))

class SendResponse(dict):
    def __init__(self, dict_):
        super(SendResponse, self).__init__(dict_)
        self['sent_text'] = cast_to_type(unicode, self['sent_text'])
        self['parts_count'] = cast_to_type(int, self['parts_count'])
        assert len(self['message_id']), 'message_id cannot be empty!'
        for key in self['message_id'].iterkeys():
            self['message_id'][key] = cast_to_type(unicode, self['message_id'][key])

class AccountResponse(dict):
    def __init__(self, dict_):
        super(AccountResponse, self).__init__(dict_)
        self['balance'] = cast_to_type(float, self['balance'])

class ReceiveResponse(dict):
    def __init__(self, dict_):
        super(ReceiveResponse, self).__init__(dict_)
        self['unread'] = cast_to_type(int, self['unread'])
        for message in self['messages']:
            message['message_id'] = cast_to_type(unicode, message['message_id'])
            message['from'] = cast_to_type(unicode, message['from'])
            message['text'] = cast_to_type(unicode, message['text'])
            message['timestamp'] = time_or_none(message['timestamp'])

class MessageStatusResponse(dict):
    def __init__(self, dict_):
        super(MessageStatusResponse, self).__init__(dict_)
        for key in self.iterkeys():
            self[key]['text'] = cast_to_type(unicode, self[key]['text'])
            self[key]['status'] = cast_to_type(unicode, self[key]['status'])
            self[key]['created_time'] = time_or_none(self[key]['created_time'])
            self[key]['reply_number'] = cast_to_type(unicode, self[key]['reply_number'])
            if self[key].has_key('completed_time'):
                self[key]['completed_time'] = time_or_none(self[key]['completed_time'])
                self[key]['credits_cost'] = cast_to_type(float, self[key]['credits_cost'])

class DeleteReplyResponse(dict):
    def __init__(self, dict_):
        super(DeleteReplyResponse, self).__init__(dict_)
        for idx in xrange(len(self['deleted'])):
            self['deleted'][idx] = cast_to_type(unicode, self['deleted'][idx])

class StatusCallbackResponse(dict):

    def __init__(self, dict_):
        super(StatusCallbackResponse, self).__init__(dict_)
        self['status'] = cast_to_type(unicode, self['status'])
        self['message_id'] = cast_to_type(unicode, self['message_id'])
        self['timestamp'] = time_or_none(self['timestamp'])
        self['credits_cost'] = cast_to_type(float, self['credits_cost'])

class ReplyCallbackResponse(dict):

    def __init__(self, dict_):
        super(ReplyCallbackResponse, self).__init__(dict_)
        self['message_id'] = cast_to_type(unicode, self['message_id'])
        self['text'] = cast_to_type(unicode, self['text'].decode('utf-8'))
        self['timestamp'] = time_or_none(self['timestamp'])
        self['from'] = cast_to_type(unicode, self['from'])

class TextMagicError(Exception):
    def __init__(self, dict_):
        self.code = cast_to_type(int, dict_['error_code'])
        self.message = cast_to_type(unicode, dict_['error_message'])

    def __str__(self):
        return "%d: %s" % (self.code, self.message)
