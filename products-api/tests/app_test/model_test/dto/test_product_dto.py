import unittest
from app.model.dto.product_dto import ProductDto
from app.model.product import Product


class ProductDtoTest(unittest.TestCase):

    def test_should_parse_product_dto_when_is_filled(self):
        product_dto: ProductDto = ProductDto()
        product_dto.name = "teste"
        product_dto.categories = ["CAT1", "cozinha"]
        product_dto.price = 1.0
        product_dto.url = "teste"

        product: Product = product_dto.parse_to_product()

        self.assertEqual(product_dto.name, product.name)
        self.assertEqual(product_dto.categories, product.categories)
        self.assertEqual(product_dto.price, product.price)
        self.assertEqual(product_dto.url, product.url)

if __name__ == '__main__':
    unittest.main()
