from textmagic.test import TextMagicTestsBase

class AccountTests(TextMagicTestsBase):
    def testAccount(self):
        result = self.client.account()
        expected_keys = set(['balance'])
        self.assertEquals(set(result.keys()), expected_keys)
        try:
            float(result['balance'])
        except:
            self.fail('balance should be a float!')
