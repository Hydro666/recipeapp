import abc
import dataclasses

@dataclasses.dataclass
class StructuredRecipe:
    name: str
    recipe_ingredients: list[tuple[int, str]]


class DataAccessClient:

    @abc.abstractmethod
    def create_recipe(self, recipe: StructuredRecipe):
        ...

    # @abc.abstractmethod
    def get_recipe(self, recipe_name: str) -> StructuredRecipe:
        ...

    # @abc.abstractmethod
    def update_recipe(self, recipe: StructuredRecipe):
        ...

    # @abc.abstractmethod
    def delete_recipe(self, recipe_name: str):
        ...

