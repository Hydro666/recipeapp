import dataclasses

@dataclasses.dataclass
class StructuredRecipe:
    name: str
    recipe_ingredients: list[tuple[int, str]]


class DataAccessClient:

    def __init__(self):
        pass

    def create_recipe(self, recipe: StructuredRecipe):
        pass

    def get_recipe(self, recipe_name: str) -> StructuredRecipe:
        pass

    def update_recipe(self, recipe: StructuredRecipe):
        pass

    def delete_recipe(self, recipe_name: str):
        pass

