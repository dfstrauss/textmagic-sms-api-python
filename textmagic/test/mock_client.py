"""
This module contains one class MockTextMagicClient to run tests against.

The MockTextMagicClient class implements the same interface as the "real"
TextMagicClient class. It is used to run tests without the need for connecting
to the live system.

On startup, MockTextMagicClient reads a file called mock_client_scenarios.txt
containing requests and responses as needed by the tests. New scenarios can be
collected for this file by running "live" tests and copying scenarios from
executed_commands.log.

"""
import urllib

from textmagic.client import _TextMagicClientBase

from textmagic import import_json
json = import_json()

class MockTextMagicClient(_TextMagicClientBase):

    def __init__(self, username, password):
        super(MockTextMagicClient, self).__init__(username, password)
        self.loadCannedResponses()

    @classmethod
    def loadCannedResponses(self):
        self.canned_responses = list()
        lines = open('mock_client_scenarios.txt').readlines()
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if line.startswith('Parameters:'):
                params = line[11:].strip()
                idx += 1
                line = lines[idx]
                assert line.startswith('Response:')
                response = line[9:].strip()
                parameters = {}
                for param in params.split('&'):
                    name, value = param.split('=')
                    parameters[name] = urllib.unquote_plus(value)
                del parameters['username']
                del parameters['password']
                self.canned_responses.append([parameters, response])
            idx += 1

    def _submitRequest(self, params_dict):
        possible_responses = [response[1] for response in self.canned_responses if response[0] == params_dict]
        assert len(possible_responses) > 0
        del self.canned_responses[self.canned_responses.index([params_dict, possible_responses[0]])]
        return possible_responses[0]
