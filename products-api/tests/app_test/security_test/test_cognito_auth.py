import unittest

from app.security import cognito_auth
from exceptions import ApiException, exceptions


class CognitoAuthTest(unittest.TestCase):

    DEFAULT_NONE_TOKEN = None
    DEFAULT_WITHOUT_BEARER_TOKEN = "eyJraWQiOiJubEtjQ1JMXC94SVdYc3ljODZFSzhHaXQ0ekhlUFpIYW9Ha2RIMTF5K3pmST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZjQ4N2U3Ni01NzdhLTRhNDgtOGI0Yi05ZTRiZjM3NzVlYmIiLCJhdWQiOiIyaHE4MTNkOHRpbnVzbTRwaWY5YnYwaTR1OSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6IjJiOTUzZjM1LTljZjAtNDViMi1iYWJjLTNhODhlZGY1MmQwMiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTcyMjU2OTM4LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9Qb3dmRVdON3AiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ3VpbGhlcm1lZ2luZXpzaWx2YSIsImV4cCI6MTU3MjI2MDUzOCwiaWF0IjoxNTcyMjU2OTM5LCJlbWFpbCI6Imd1aWxoZXJtZWdpbmV6c2lsdmFAZ21haWwuY29tIn0.s4n08YI9KUkuF3DYRWKgT_y4i2AUi7gGfo-GA8J_gxQJhlRi4T4g8nQgTgDUy9pAWTbs_a6ELlSL7Vec9GvDtmKV47k7mbSC-_DFNhbds7v2n22W3KYfc7P_mx97cKqhImmj0x5nhaTES22ogOstFF9EjjtRwxwEyh9ZSXG08ymwkxoP3cKAzy1-QrN5Ew61ZqCnifyzqUbmYe8-rhT-xvkaVRhoqUsVHkxu5-w2YV9UE-4KGsVLRqfsvG1GlBgcSZc4_5IhsOmzy0odl4CHgrQe_mspJ8kZikCG6ZWe-mTwpSZx4tEAxcQlMHRK93qJ5BaUik1r3FnWtJIZPdyy9w"
    DEFAULT_WITH_EMPTY_TOKEN = ""

    def test_should_raise_authentication_exception_when_token_is_invalid(self):
        expected_exception = exceptions.get(exceptions.USER_NOT_AUTHORIZED_EXCEPTION)

        with self.assertRaises(ApiException) as context:
            cognito_auth.verify_token(self.DEFAULT_NONE_TOKEN)

        self.assertEqual(expected_exception.code, context.exception.code)

        with self.assertRaises(ApiException) as context:
            cognito_auth.verify_token(self.DEFAULT_WITHOUT_BEARER_TOKEN)

        self.assertEqual(expected_exception.code, context.exception.code)

        with self.assertRaises(ApiException) as context:
            cognito_auth.verify_token(self.DEFAULT_WITH_EMPTY_TOKEN)

        self.assertEqual(expected_exception.code, context.exception.code)

if __name__ == '__main__':
    unittest.main()
