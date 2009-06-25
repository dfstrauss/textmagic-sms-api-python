from textmagic.test import TextMagicTestsBase

class CheckNumberTests(TextMagicTestsBase):

    za_number = '27123456789'
    gb_number = '44123456789'

    def testCheckTwoNumbers(self):
        result = self.client.check_number([self.za_number, self.gb_number])
        expected_keys = set([self.za_number, self.gb_number])
        self.assertEquals(set(result.keys()), expected_keys)
        self.assertTrue(isinstance(result[self.za_number]['price'], float))
        self.assertEquals(result[self.za_number]['country'], 'ZA')
        self.assertTrue(isinstance(result[self.gb_number]['price'], float))
        self.assertEquals(result[self.gb_number]['country'], 'GB')

    def testCheckOneNumber(self):
        result = self.client.check_number(self.za_number)
        expected_keys = set([self.za_number])
        self.assertEquals(set(result.keys()), expected_keys)
        self.assertTrue(isinstance(result[self.za_number]['price'], float))
        self.assertEquals(result[self.za_number]['country'], 'ZA')
