from textmagic.test import TextMagicTestsBase

class AccountTests(TextMagicTestsBase):
    def testAccount(self):
        result = self.client.account()
        expected_keys = set(['balance'])
        self.assertEquals(set(result), expected_keys)
        try:
            float(result['balance'])
        except TypeError:
            self.fail('balance should be a float!')
