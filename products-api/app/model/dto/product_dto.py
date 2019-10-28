from typing import List

from fastapi import Query
from pydantic import BaseModel

from app.model import category
from app.model.product import Product
from exceptions import exceptions
from validator import validators


class ProductDto(BaseModel):
    name: str = Query(None)
    categories: List[str] = Query(None)
    price: float = Query(None)
    url: str = Query(None)

    def parse_to_product(self) -> Product:
        return Product(
            self.name,
            self.categories,
            self.price,
            self.url
        )

    def _get_url_prefix(self, name: str):
        return name.replace(" ", "-")


class ProductCreateDto(ProductDto):

    def validate_model(self) -> None:
        self.__validate_structure()
        self.__validate_values()

    def __validate_structure(self) -> None:
        exception = exceptions.get(exceptions.FIELD_CONSTRAINT_VIOLATION_EXCEPTION)
        if validators.is_none(self.name):
            exception.append_validation_error("O campo é obrigatório", "name")
        if validators.is_none(self.url):
            exception.append_validation_error("O campo é obrigatório", "url")

        if exception.has_validation_errors():
            raise exception

    def __validate_values(self) -> None:
        exception = exceptions.get(exceptions.FIELD_VALUE_CONSTRAINT_VIOLATION_EXCEPTION)

        if not validators.in_range(len(self.name), 3, 50):
            exception.append_validation_error("Deve ter no mínimo 3 e no máximo 50 caracteres", "name")

        if validators.match(self.name, "^[A-Z|a-z].*[A-Z|a-z]$"):
            exception.append_validation_error("O nome não pode começar ou terminar com letras", "name")

        if not validators.contains_values(category.AVAILABLE_CATEGORIES, self.categories):
            exception.append_validation_error("Uma ou mais categorias solicitadas não existem, "
                                              "favor usar apenas categorias existentes: {}"
                                              .format(str(category.AVAILABLE_CATEGORIES)), "categories")

        if self.price:
            if not validators.in_range(self.price, 1.99, 5000.00):
                exception.append_validation_error("O preço precisa ser no mínimo 1.99 e no máximo 5000.00", "price")

        if not validators.match(self.url, self._get_url_prefix("{}.*".format(self.name))):
            exception.append_validation_error("A url deve começar com o nome hifienizado", "url")

        if not validators.in_range(len(self.url), 30, 120):
            exception.append_validation_error("Deve ter no mínimo 3 e no máximo 50 caracteres", "url")

        if exception.has_validation_errors():
            raise exception


class ProductUpdateDto(ProductCreateDto):
    pass


class ProductPatchDto(ProductCreateDto):
    def validate_model(self) -> None:
        self.__validate_values()

    def __validate_values(self) -> None:
        exception = exceptions.get(exceptions.FIELD_VALUE_CONSTRAINT_VIOLATION_EXCEPTION)

        if self.name:
            if not validators.in_range(len(self.name), 3, 50):
                exception.append_validation_error("Deve ter no mínimo 3 e no máximo 50 caracteres", "name")

            if validators.match(self.name, "^[A-Z|a-z].*[A-Z|a-z]$"):
                exception.append_validation_error("O nome não pode começar ou terminar com letras", "name")

        if self.categories:
            if not validators.contains_values(category.AVAILABLE_CATEGORIES, self.categories):
                exception.append_validation_error("Uma ou mais categorias solicitadas não existem, "
                                                  "favor usar apenas categorias existentes: {}"
                                                  .format(str(category.AVAILABLE_CATEGORIES)), "categories")
        if self.price:
            if self.price:
                if not validators.in_range(self.price, 1.99, 5000.00):
                    exception.append_validation_error("O preço precisa ser no mínimo 1.99 e no máximo 5000.00", "price")

        if self.url:
            if not self.name:
                exception.append_validation_error("O campo name deve ser enviado quando for atualizar a url", "url")

            if not validators.match(self.url, self._get_url_prefix("{}.*".format(self.name))):
                exception.append_validation_error("A url deve começar com o nome hifienizado", "url")

            if not validators.in_range(len(self.url), 30, 120):
                exception.append_validation_error("Deve ter no mínimo 3 e no máximo 50 caracteres", "url")

        if exception.has_validation_errors():
            raise exception
