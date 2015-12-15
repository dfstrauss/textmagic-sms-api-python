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
import urllib.request, urllib.parse, urllib.error

from textmagic.client import _TextMagicClientBase

from textmagic import import_json
json = import_json()


class MockTextMagicClient(_TextMagicClientBase):

    @classmethod
    def _load_canned_responses(self):
        self.canned_responses = list()
        params_start = 'Parameters:'
        response_start = 'Response:'
        scenarios_file = open('mock_client_scenarios.txt')
        for line in scenarios_file:
            if line.startswith(params_start):
                params = line[len(params_start):].strip()
                # A "Response:" line must follow a "Parameters:" line
                line = next(scenarios_file)
                assert line.startswith(response_start)
                response = line[len(response_start):].strip()
                parameters = {}
                for param in params.split('&'):
                    name, value = param.split('=')
                    parameters[name] = urllib.parse.unquote_plus(value)
                del parameters['username']
                del parameters['password']
                self.canned_responses.append([parameters, response])
        scenarios_file.close()

    def __init__(self, username, password):
        super(MockTextMagicClient, self).__init__(username, password)
        self._load_canned_responses()

    def _submit_request(self, params_dict):
        possible_responses = [response[1] for response in self.canned_responses if response[0] == params_dict]
        assert len(possible_responses) > 0
        del self.canned_responses[self.canned_responses.index([params_dict, possible_responses[0]])]
        return possible_responses[0]
