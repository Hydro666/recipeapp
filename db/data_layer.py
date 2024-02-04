import abc
from typing import NamedTuple


class RecipeIngredient(NamedTuple):
    name: str
    quantity: int


class StructuredRecipe(NamedTuple):
    name: str
    recipe_ingredients: set[RecipeIngredient]


class DataAccessClient:

    @abc.abstractmethod
    def create_recipe(self, recipe: StructuredRecipe): ...

    @abc.abstractmethod
    def get_recipe(self, recipe_name: str) -> StructuredRecipe: ...

    # @abc.abstractmethod
    def update_recipe(self, recipe: StructuredRecipe): ...

    # @abc.abstractmethod
    def delete_recipe(self, recipe_name: str): ...
