"""
Run tests for the TextMagic python API wrapper. Tests can be run "live"
against the TextMagic system, or against a "local" mock implementation.

Parameters:
-h --help       Print this message
-l --live       Run tests "live" against TextMagic system (otherwise run
                against mock client)
-u --username   TextMagic API username (must be provided for "live" tests)
-p --password   TextMagic API password (must be provided for "live" tests)

"""

__author__ = "Dawie Strauss"
__copyright__ = "Copyright 2009, TextMagic Ltd"
__license__ = "BSD"

import getopt
import sys
import unittest

import textmagic.test.mock_client
import textmagic.test.send
import textmagic.test.account
import textmagic.test.message_status
import textmagic.test.receive
import textmagic.test.delete_reply
import textmagic.test.other
import textmagic.test.callbacks
import textmagic.test.responses

def usage():
    print "Usage: main.py\n%s" % __doc__

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlu:p:", ["help", "live", "username=", "password="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-l", "--live"):
            textmagic.test.running_live = True
            textmagic.test.client_class = textmagic.client.TextMagicClient
            textmagic.test.log_executed_commands = True
        elif o in ("-u", "--username"):
            textmagic.test.api_username = a
        elif o in ("-p", "--password"):
            textmagic.test.api_password = a
        else:
            assert False, "unhandled option"

    if (textmagic.test.client_class <> textmagic.client.TextMagicClient):
        textmagic.test.log_executed_commands = False

    suite = unittest.TestSuite()
    tests = [
        textmagic.test.send.BasicSendTests,
        textmagic.test.send.MultipartUnicodeSendTests,
        textmagic.test.send.MultipartGsm0338SendTests,
        textmagic.test.send.MaxLengthSendTests,
        textmagic.test.send.SendCharacterSetsTests,
        textmagic.test.send.SendTimeTests,
        textmagic.test.send.SendErrorsTests,
        textmagic.test.account.AccountTests,
        textmagic.test.message_status.MessageStatusTests,
        textmagic.test.receive.ReceiveTests,
        textmagic.test.delete_reply.DeleteReplyTests,
        textmagic.test.delete_reply.DeleteReplyErrorsTests,
        textmagic.test.other.ParameterErrorTests,
        textmagic.test.other.Gsm0338CharacterSetTests,
        textmagic.test.callbacks.CallbackUrlTests,
        textmagic.test.responses.TextMagicResponseTests,
    ]
## Uncomment to run only BasicSendTests
#    tests = [
#        textmagic.test.send.BasicSendTests,
#    ]
    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
    