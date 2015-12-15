from textmagic.test import TextMagicTestsBase
from textmagic.test import LiveUnsafeTests
from textmagic.client import TextMagicError


class DeleteReplyTests(TextMagicTestsBase, LiveUnsafeTests):

    def deleteIds(self, ids):
        response = self.client.delete_reply(ids)
        if not isinstance(ids, list):
            ids = [ids]
        self.assertKeysEqualExpectedKeys(response, ['deleted'])
        self.assertEquals(
            set(response['deleted']),
            set([str(id) for id in ids]))

    def testDeleteOneMessage(self):
        self.deleteIds(1787522)

    def testDeleteTwoMessages(self):
        self.deleteIds([1787548,"1787572"])

    def testDeletingNonExistentMessagesFail(self):
        try:
            self.client.delete_reply([1787548,1787573])
            self.fail('An error is expected to skip this line')
        except TextMagicError as e:
            self.assertEquals(e.error_code, 14)
            self.assertEquals(e.error_message, 'Message with id 1787548, 1787573 does not exist')


class DeleteReplyErrorsTests(TextMagicTestsBase):
    """
    Test error messages on deleting.

    """

    def testTryingToDeleteTooManyItems(self):
        try:
            self.client.delete_reply(['5111%03d' % num for num in range(101)])
            self.fail('An error is expected to skip this line')
        except TextMagicError as e:
            self.assertEquals(e.error_code, 12)
            self.assertEquals(e.error_message, 'Too many items in one request')
