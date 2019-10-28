import copy
import unittest
from unittest.mock import patch

from starlette.responses import Response

import products_api_server
from app.model.auth_user import AuthUser
from app.model.dto.product_dto import ProductCreateDto, ProductPatchDto, ProductUpdateDto
from app.model.product import Product
from exceptions import exceptions


class ProductsApiServerTest(unittest.TestCase):

    DEFAULT_RESPONSE_DICT = Response()
    #     {
    #     status_code: 000,
    #     "body": {}
    # }
    DEFAULT_AUTH_TOKEN = "eyJraWQiOiJubEtjQ1JMXC94SVdYc3ljODZFSzhHaXQ0ekhlUFpIYW9Ha2RIMTF5K3pmST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZjQ4N2U3Ni01NzdhLTRhNDgtOGI0Yi05ZTRiZjM3NzVlYmIiLCJhdWQiOiIyaHE4MTNkOHRpbnVzbTRwaWY5YnYwaTR1OSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6IjJiOTUzZjM1LTljZjAtNDViMi1iYWJjLTNhODhlZGY1MmQwMiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTcyMjU2OTM4LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9Qb3dmRVdON3AiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ3VpbGhlcm1lZ2luZXpzaWx2YSIsImV4cCI6MTU3MjI2MDUzOCwiaWF0IjoxNTcyMjU2OTM5LCJlbWFpbCI6Imd1aWxoZXJtZWdpbmV6c2lsdmFAZ21haWwuY29tIn0.s4n08YI9KUkuF3DYRWKgT_y4i2AUi7gGfo-GA8J_gxQJhlRi4T4g8nQgTgDUy9pAWTbs_a6ELlSL7Vec9GvDtmKV47k7mbSC-_DFNhbds7v2n22W3KYfc7P_mx97cKqhImmj0x5nhaTES22ogOstFF9EjjtRwxwEyh9ZSXG08ymwkxoP3cKAzy1-QrN5Ew61ZqCnifyzqUbmYe8-rhT-xvkaVRhoqUsVHkxu5-w2YV9UE-4KGsVLRqfsvG1GlBgcSZc4_5IhsOmzy0odl4CHgrQe_mspJ8kZikCG6ZWe-mTwpSZx4tEAxcQlMHRK93qJ5BaUik1r3FnWtJIZPdyy9w"

    DEFAULT_PRODUCT_ID = "60dd920c-e1ef-4afe-894a-f04ef3c116c8"
    DEFAULT_PRODUCT_NAME = "5PRODUCT TEST"
    DEFAULT_PRODUCT_PRICE = 6.99
    DEFAULT_PRODUCT_URL = "5PRODUCT-TESTfdasfdasfahgfhgfdhfgdhdfghgfdhfdghfgdhfdghfdghfdghfdghfdghdf"
    DEFAULT_PRODUCT_CATEGORIES = ["eletrônicos",
                                   "utensílios",
                                   "cama e mesa",
                                   "cozinha",
                                   "higiene pessoal",
                                   "abobrinha"
                                  ]

    DEFAULT_UPDATE_PRODUCT_NAME = "5PRODUCT TEST2"
    DEFAULT_UPDATE_PRODUCT_CATEGORIES = ["eletrônicos",
                                   "utensílios",
                                   "cama e mesa",
                                   "abobrinha"
                                  ]
    DEFAULT_UPDATE_PRODUCT_PRICE = 10.0
    DEFAULT_UPDATE_PRODUCT_URL = "5PRODUCT-TEST2fdasfdasfahgfhgfdhfgdhdfghgfdhfdghfgdhfdghfdghfdghfdghfdghdf"

    DEFAULT_2_PRODUCTS_ARRAY: [] = [
        Product(
            DEFAULT_PRODUCT_NAME,
            DEFAULT_PRODUCT_CATEGORIES,
            DEFAULT_PRODUCT_PRICE,
            DEFAULT_PRODUCT_URL,
            DEFAULT_PRODUCT_ID
        ),
        Product(
            DEFAULT_PRODUCT_NAME,
            DEFAULT_PRODUCT_CATEGORIES,
            DEFAULT_PRODUCT_PRICE,
            DEFAULT_PRODUCT_URL,
            DEFAULT_PRODUCT_ID
        )
    ]

    DEFAULT_INVALID_PRODUCT_CREATE_DTO = ProductCreateDto()
    DEFAULT_INVALID_PRODUCT_CREATE_DTO.name = ""
    DEFAULT_INVALID_PRODUCT_CREATE_DTO.categories = ["CAT1", "cozinha"]
    DEFAULT_INVALID_PRODUCT_CREATE_DTO.price = 1.0
    DEFAULT_INVALID_PRODUCT_CREATE_DTO.url = "sgfsdgsd"

    DEFAULT_PRODUCT_CREATE_DTO = ProductCreateDto()
    DEFAULT_PRODUCT_CREATE_DTO.name = DEFAULT_PRODUCT_NAME
    DEFAULT_PRODUCT_CREATE_DTO.categories = DEFAULT_PRODUCT_CATEGORIES
    DEFAULT_PRODUCT_CREATE_DTO.price = DEFAULT_PRODUCT_PRICE
    DEFAULT_PRODUCT_CREATE_DTO.url = DEFAULT_PRODUCT_URL

    DEFAULT_PRODUCT_UPDATE_DTO = ProductUpdateDto()
    DEFAULT_PRODUCT_UPDATE_DTO.name = DEFAULT_UPDATE_PRODUCT_NAME
    DEFAULT_PRODUCT_UPDATE_DTO.categories = DEFAULT_UPDATE_PRODUCT_CATEGORIES
    DEFAULT_PRODUCT_UPDATE_DTO.price = DEFAULT_UPDATE_PRODUCT_PRICE
    DEFAULT_PRODUCT_UPDATE_DTO.url = DEFAULT_UPDATE_PRODUCT_URL

    DEFAULT_INVALID_PRODUCT_UPDATE_DTO = ProductCreateDto()
    DEFAULT_INVALID_PRODUCT_UPDATE_DTO.name = ""
    DEFAULT_INVALID_PRODUCT_UPDATE_DTO.categories = ["CAT2", "utensílios"]
    DEFAULT_INVALID_PRODUCT_UPDATE_DTO.price = 1.0
    DEFAULT_INVALID_PRODUCT_UPDATE_DTO.url = "sgfsdgsd"

    DEFAULT_PRODUCT_PATCH_DTO = ProductPatchDto()
    DEFAULT_PRODUCT_PATCH_DTO.name = None
    DEFAULT_PRODUCT_PATCH_DTO.categories = DEFAULT_UPDATE_PRODUCT_CATEGORIES
    DEFAULT_PRODUCT_PATCH_DTO.price = DEFAULT_UPDATE_PRODUCT_PRICE
    DEFAULT_PRODUCT_PATCH_DTO.url = None

    DEFAULT_INVALID_PRODUCT_PATCH_DTO = ProductCreateDto()
    DEFAULT_INVALID_PRODUCT_PATCH_DTO.name = ""
    DEFAULT_INVALID_PRODUCT_PATCH_DTO.categories = ["CAT2", "utensílios"]
    DEFAULT_INVALID_PRODUCT_PATCH_DTO.price = 1.0
    DEFAULT_INVALID_PRODUCT_PATCH_DTO.url = "sgfsdgsd"

    DEFAULT_INVALID_PRODUCT_PATCH_NO_NAME_WITH_URL_DTO = ProductCreateDto()
    DEFAULT_INVALID_PRODUCT_PATCH_NO_NAME_WITH_URL_DTO.categories = ["CAT2", "utensílios"]
    DEFAULT_INVALID_PRODUCT_PATCH_NO_NAME_WITH_URL_DTO.price = 1.0
    DEFAULT_INVALID_PRODUCT_PATCH_NO_NAME_WITH_URL_DTO.url = "sgfsdgsd"

    DEFAULT_AUTH_USER = AuthUser("b9225de5-3090-48c5-9200-94f8039384ff", "teste@gmail.com")

    @patch('app.products_service.delete_product', autospec=True)
    @patch('app.products_service.update_product', autospec=True)
    @patch('app.products_service.create_product', autospec=True)
    @patch('app.products_service.get_product', autospec=True)
    @patch('app.products_service.get_products', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_get_contraint_exception_when_constraints_fails(
            self,
            verify_token_mock,
            get_products_mock,
            get_product_mock,
            create_product_mock,
            update_product_mock,
            delete_product_mock
    ):
        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)

        expected_exception = exceptions.get(exceptions.FIELD_CONSTRAINT_VIOLATION_EXCEPTION)

        exception_json_body = products_api_server.get_product(
            None,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEquals(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(1, len(exception_json_body["validationErrors"]))

        exception_json_body = products_api_server.get_product(
            "fdasfasmdfmsafas",
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEquals(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(1, len(exception_json_body["validationErrors"]))

        dto = copy.deepcopy(self.DEFAULT_INVALID_PRODUCT_CREATE_DTO)
        exception_json_body = products_api_server.create_product(
            dto,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(4, len(exception_json_body["validationErrors"]))

        dto = copy.deepcopy(self.DEFAULT_INVALID_PRODUCT_UPDATE_DTO)
        exception_json_body = products_api_server.update_product(
            self.DEFAULT_PRODUCT_ID,
            dto,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(4, len(exception_json_body["validationErrors"]))

        dto = copy.deepcopy(self.DEFAULT_INVALID_PRODUCT_PATCH_DTO)
        exception_json_body = products_api_server.update_product(
            self.DEFAULT_PRODUCT_ID,
            dto,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(4, len(exception_json_body["validationErrors"]))

        dto = copy.deepcopy(self.DEFAULT_INVALID_PRODUCT_PATCH_NO_NAME_WITH_URL_DTO)
        exception_json_body = products_api_server.update_product(
            self.DEFAULT_PRODUCT_ID,
            dto,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(1, len(exception_json_body["validationErrors"]))

        exception_json_body = products_api_server.delete_product(
            None,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(expected_exception.code, exception_json_body["errorCode"])
        self.assertEquals(1, len(exception_json_body["validationErrors"]))


    @patch('app.products_service.delete_product', autospec=True)
    @patch('app.products_service.update_product', autospec=True)
    @patch('app.products_service.create_product', autospec=True)
    @patch('app.products_service.get_product', autospec=True)
    @patch('app.products_service.get_products', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_get_authentication_exception_response_when_authentication_fails(
            self,
            verify_token_mock,
            get_products_mock,
            get_product_mock,
            create_product_mock,
            update_product_mock,
            delete_product_mock

    ):
        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        exception = exceptions.get(exceptions.USER_NOT_AUTHORIZED_EXCEPTION)

        get_products_mock.side_effect = exception
        get_product_mock.side_effect = exception
        create_product_mock.side_effect = exception
        update_product_mock.side_effect = exception
        delete_product_mock.side_effect = exception

        exception_json_body = products_api_server.get_all_products(
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(exception.code, exception_json_body["errorCode"])

        exception_json_body = products_api_server.get_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(exception.code, exception_json_body["errorCode"])

        exception_json_body = products_api_server.create_product(
            self.DEFAULT_PRODUCT_CREATE_DTO,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(exception.code, exception_json_body["errorCode"])

        exception_json_body = products_api_server.update_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_PRODUCT_UPDATE_DTO,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(exception.code, exception_json_body["errorCode"])

        exception_json_body = products_api_server.patch_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_PRODUCT_PATCH_DTO,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(exception.code, exception_json_body["errorCode"])

        exception_json_body = products_api_server.delete_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEqual(exception.code, exception_json_body["errorCode"])

    @patch('app.products_service.get_products', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_get_all_products_when_products_available(self, verify_token_mock, get_products_mock):

        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        get_products_mock.return_value = copy.deepcopy(self.DEFAULT_2_PRODUCTS_ARRAY)

        products: [] = products_api_server.get_all_products(
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )

        for i in range(len(products)):
            self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[i].name, products[i].name)
            self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[i].categories, products[i].categories)
            self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[i].price, products[i].price)
            self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[i].url, products[i].url)

    @patch('app.products_service.get_product', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_get_product_when_product_exists(self, verify_token_mock, get_products_mock):

        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        get_products_mock.return_value = copy.deepcopy(self.DEFAULT_2_PRODUCTS_ARRAY[0])

        product: Product = products_api_server.get_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )

        self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[0].name, product.name)
        self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[0].categories, product.categories)
        self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[0].price, product.price)
        self.assertEqual(self.DEFAULT_2_PRODUCTS_ARRAY[0].url, product.url)

    @patch('app.products_service.get_product', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_get_product_when_method_is_called(self, verify_token_mock, get_products_mock):

        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)

        exception = exceptions.get(exceptions.PRODUCT_NOT_FOUND_EXCEPTION)
        get_products_mock.side_effect = exception

        exception_json_body = products_api_server.get_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )
        self.assertEquals(exception.code, exception_json_body["errorCode"])

    @patch('app.products_service.create_product', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_create_product_when_product_is_ok(self, verify_token_mock, create_product_mock):

        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        create_product_mock.return_value = None

        products_api_server.create_product(
            self.DEFAULT_PRODUCT_CREATE_DTO,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )

        create_product_mock.assert_called_once()

    @patch('app.products_service.update_product', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_update_product_when_product_is_ok(self, verify_token_mock, update_product_mock):
        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        update_product_mock.return_value = None

        products_api_server.update_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_PRODUCT_UPDATE_DTO,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )

        update_product_mock.assert_called_once()

    @patch('app.products_service.update_product', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_patch_product_when_product_is_ok(self, verify_token_mock, update_product_mock):
        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        update_product_mock.return_value = None

        products_api_server.patch_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_PRODUCT_PATCH_DTO,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )

        update_product_mock.assert_called_once()

    @patch('app.products_service.delete_product', autospec=True)
    @patch('app.security.cognito_auth.verify_token', autospec=True)
    def test_should_delete_product_when_product_is_ok(self, verify_token_mock, delete_product_mock):
        verify_token_mock.return_value = copy.deepcopy(self.DEFAULT_AUTH_USER)
        delete_product_mock.return_value = None

        products_api_server.delete_product(
            self.DEFAULT_PRODUCT_ID,
            self.DEFAULT_RESPONSE_DICT,
            self.DEFAULT_AUTH_TOKEN
        )

        delete_product_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
