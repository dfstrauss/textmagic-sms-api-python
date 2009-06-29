"""
Run tests for the TextMagic python API wrapper. Tests can be run "live"
against the TextMagic system, or against a "local" mock implementation.

When running "live" certain tests are omitted, because they cannot run "live"
unchanged. E.g. "delete" tests have hard-coded message ids which they try to
delete.

Also when tests run "live", all requests and responses are logged to a file
called executed_commands.log

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
import textmagic.test.send_tests
import textmagic.test.account_tests
import textmagic.test.message_status_tests
import textmagic.test.receive_tests
import textmagic.test.delete_reply_tests
import textmagic.test.check_number_tests
import textmagic.test.other_tests
import textmagic.test.callbacks_tests
import textmagic.test.responses_tests

from textmagic.test import LiveUnsafeTests

def usage():
    print "Usage: test_client.py\n%s" % __doc__

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

    suite = unittest.TestSuite()
    tests = [
        textmagic.test.send_tests.BasicSendTests,
        textmagic.test.send_tests.MultipartUnicodeSendTests,
        textmagic.test.send_tests.MultipartGsm0338SendTests,
        textmagic.test.send_tests.MaxLengthSendTests,
        textmagic.test.send_tests.SendCharacterSetsTests,
        textmagic.test.send_tests.SendTimeTests,
        textmagic.test.send_tests.SendErrorsTests,
        textmagic.test.account_tests.AccountTests,
        textmagic.test.message_status_tests.MessageStatusTests,
        textmagic.test.message_status_tests.LiveUnsafeMessageStatusTests,
        textmagic.test.receive_tests.ReceiveTests,
        textmagic.test.receive_tests.LiveUnsafeReceiveTests,
        textmagic.test.delete_reply_tests.DeleteReplyTests,
        textmagic.test.delete_reply_tests.DeleteReplyErrorsTests,
        textmagic.test.check_number_tests.CheckNumberTests,
        textmagic.test.other_tests.ParameterErrorTests,
        textmagic.test.other_tests.Gsm0338CharacterSetTests,
        textmagic.test.callbacks_tests.CallbackUrlTests,
        textmagic.test.responses_tests.TextMagicResponseTests,
    ]
## Uncomment to run only BasicSendTests
#    tests = [
#        textmagic.test.send_tests.BasicSendTests,
#    ]
    for test in tests:
        # Filter out live-unsafe tests when running live
        if (textmagic.test.running_live and\
            not LiveUnsafeTests in test.__bases__) or\
            not textmagic.test.running_live:
                suite.addTest(unittest.makeSuite(test))

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
    