import unittest
from app.model import category


class CategoryTest(unittest.TestCase):

    TEST_AVAILABLE_CATEGORIES = [
        "eletrônicos",
        "utensílios",
        "cama e mesa",
        "cozinha",
        "higiene pessoal",
        "abobrinha"
    ]

    TEST_UNAVAILABLE_CATEGORIES = [
        "cat1",
        "asfdas",
        "lkjhljh",
        "64564654",
        None
    ]

    def test_should_return_true_when_category_is_available(self):

        for cat in self.TEST_AVAILABLE_CATEGORIES:
            self.assertTrue(category.is_available(cat))

        for cat in self.TEST_UNAVAILABLE_CATEGORIES:
            self.assertFalse(category.is_available(cat))


if __name__ == '__main__':
    unittest.main()
