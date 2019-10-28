import unittest
from unittest import mock
from unittest.mock import patch
from app.model.product import Product
from app import products_service


class ProductsServiceTest(unittest.TestCase):

    @patch('app.database.products_dao.insert', autospec=True)
    def test_should_add_id_when_product_is_new(self, insert_mock):

        product = Product(
            None,
            None,
            None,
            None,
            None
        )

        products_service.create_product(product)
        self.assertTrue(product.id is not None)
        insert_mock.assert_called_once()

    @patch('app.database.products_dao.update', autospec=True)
    @patch('app.database.products_dao.find_one', autospec=True)
    def test_should_keep_as_is_when_update(self, find_one_mock, update_mock):

        product = Product(
            "Teste",
            [],
            5.00,
            "Teste123",
            "IDfdasiofsdaoifmiosdafa"
        )

        products_service.update_product(product, False)
        find_one_mock.assert_called_once()
        update_mock.assert_called_with(product)

    @patch('app.database.products_dao.update', autospec=True)
    @patch('app.database.products_dao.find_one', autospec=True)
    def test_should_keep_as_is_when_patch(self, find_one_mock, update_mock):

        db_product = Product(
            "Nome do BD",
            ["cat1", "cat2"],
            9.00,
            "URL do BD",
            "ID do BD"
        )

        find_one_mock.return_value = db_product

        product = Product(
            None,
            [],
            5.00,
            None,
            "IDfdasiofsdaoifmiosdafa",
        )

        products_service.update_product(product, True)
        find_one_mock.assert_called_once()
        update_mock.assert_called_with(mock.ANY)
        name, args, kwargs = update_mock.mock_calls[0]

        update_product: Product = args[0]
        self.assertEqual(db_product.name, update_product.name)
        self.assertEqual(product.categories, update_product.categories)
        self.assertEqual(product.price, update_product.price)
        self.assertEqual(db_product.url, update_product.url)
        self.assertEqual(db_product.id, update_product.id)


if __name__ == '__main__':
    unittest.main()
