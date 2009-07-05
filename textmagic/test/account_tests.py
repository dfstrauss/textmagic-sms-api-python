from textmagic.test import TextMagicTestsBase


class AccountTests(TextMagicTestsBase):
    def testAccount(self):
        response = self.client.account()
        self.assertKeysEqualExpectedKeys(response, ['balance'])
        try:
            float(response['balance'])
        except TypeError:
            self.fail('balance should be a float!')
