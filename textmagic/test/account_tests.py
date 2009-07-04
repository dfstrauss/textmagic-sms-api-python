from textmagic.test import TextMagicTestsBase

class AccountTests(TextMagicTestsBase):
    def testAccount(self):
        result = self.client.account()
        self.assertKeysEqualExpectedKeys(result, ['balance'])
        try:
            float(result['balance'])
        except TypeError:
            self.fail('balance should be a float!')
