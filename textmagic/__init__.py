"""
PyTextMagicSMS
==============

This module provides a convenient interface to the TextMagic HTTPS API to send
SMS messages.

To use the service, you need to create an account at http://www.textmagic.com/
to get a username. Once you are registered, you can retrieve your API password
from https://www.textmagic.com/app/wt/account/api/cmd/password

The TextMagic HTTPS API is described at http://api.textmagic.com/https-api

An instance of the class textmagic.client.TextMagicClient must be instantiated
with your TextMagic username and password. API commands are implemented as
methods on this class.

The API commands are:
    send
    account
    message_status
    receive
    delete_reply
    check_number

Getting started
===============

To send a message:
    client = textmagic.client.TextMagicClient('username', 'password')
    response = client.send("A test message", "9991234444")
    message_id = response['message_id'].keys()[0]

Use the message_id to get the delivery status of your message:
    response = client.message_status(message_id)
    status = response[message_id]['status']

You can receive reply messages from your TextMagic Inbox:
    response = client.receive("0")
    for message in response['messages']:
        from_number = message['from']
        text = message['text']

"""

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
