"""
This module provides a convenient interface to the TextMagic HTTPS API for
sending SMS messages.

To use the service, you need to create an account at http://www.textmagic.com/
to get a username. Once you are registered, you can retrieve your API password
from https://www.textmagic.com/app/wt/account/api/cmd/password

To send a message:
    client = textmagic.client.TextMagicClient('username', 'password')
    result = self.client.send("A test message", "9991234444")
    message_id = result['message_id']
Use the message_id to get the delivery status of your message:
    response = self.client.message_status(message_id)

The TextMagic HTTPS API is described fully at http://api.textmagic.com/https-api

Currently implemented commands are:
    send
    account
    message_status
    receive
    delete_reply

Outstanding functionality (coming soon) is:
    send_time parameter for send command
    check_number command

"""

__author__ = "Dawie Strauss"
__copyright__ = "Copyright 2009, TextMagic Ltd"
__license__ = "BSD"
__version__ = "0.0.1"
__status__ = "Development"

def import_json():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json
        except ImportError:
            try:
                from django.utils import simplejson as json
            except:
                raise ImportError("Requires either simplejson, Python 2.6 or django.utils!")
    return json
