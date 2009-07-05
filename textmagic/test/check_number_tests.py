from textmagic.test import TextMagicTestsBase


class CheckNumberTests(TextMagicTestsBase):

    za_number = '27123456789'
    gb_number = '44123456789'

    def testCheckTwoNumbers(self):
        response = self.client.check_number([self.za_number, self.gb_number])
        self.assertKeysEqualExpectedKeys(response,
            [self.za_number, self.gb_number])
        self.assertTrue(isinstance(response[self.za_number]['price'], float))
        self.assertEquals(response[self.za_number]['country'], 'ZA')
        self.assertTrue(isinstance(response[self.gb_number]['price'], float))
        self.assertEquals(response[self.gb_number]['country'], 'GB')

    def testCheckOneNumber(self):
        response = self.client.check_number(self.za_number)
        self.assertKeysEqualExpectedKeys(response, [self.za_number])
        self.assertTrue(isinstance(response[self.za_number]['price'], float))
        self.assertEquals(response[self.za_number]['country'], 'ZA')
