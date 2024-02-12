import abc
from typing import Any, NamedTuple


class RecipeIngredient(NamedTuple):
    name: str
    quantity: int


class StructuredRecipe(NamedTuple):
    name: str
    recipe_ingredients: set[RecipeIngredient]


class DataSerializer:
    """Class for serializing and deserializing a StructuredRecipe tuple as a JSON.
    
    The zero value for the `recipe_ingredients` will be the empty list and not
    null, or field absence.
    
    The order of the elements in the `recipe_ingredients` does not hold any
    semantic meaning."""

    def serialize_structured_recipe_to_json(self, recipe: StructuredRecipe) -> dict[str, Any]:
        return {
            'name': recipe.name,
            'recipe_ingredients': [
                {"name": ri.name, "quantity": ri.quantity} for ri in recipe.recipe_ingredients
            ]
        }
    
    def parse_json_to_structured_recipe(self, json: dict[str, Any]) -> StructuredRecipe:
        if set(json) != {'name', 'recipe_ingredients'}:
            raise ValueError(f"Json: {json} cannot be parsed into a structured recipe!")
        if type(json['recipe_ingredients']) is not list:
            raise ValueError(f"Json: {json} cannot be parsed into a structured recipe!")
        ris = {RecipeIngredient(x['name'], x['quantity']) for x in json['recipe_ingredients']}
        if len(ris) != len(json['recipe_ingredients']):
            raise ValueError(f"Json: {json} cannot be parsed into a structured recipe!")
        return StructuredRecipe(json['name'], ris)


class DataAccessClient:

    @abc.abstractmethod
    def create_recipe(self, recipe: StructuredRecipe): ...

    @abc.abstractmethod
    def get_recipe(self, recipe_name: str) -> StructuredRecipe: ...

    # @abc.abstractmethod
    def update_recipe(self, recipe: StructuredRecipe): ...

    # @abc.abstractmethod
    def delete_recipe(self, recipe_name: str): ...
