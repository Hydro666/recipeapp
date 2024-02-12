from absl import app
from db.sqlite import client

from db import data_layer

c = client.SQLiteClient("test_db.db")


bread_recipe = data_layer.StructuredRecipe(
    "bread",
    recipe_ingredients={
        data_layer.RecipeIngredient("flour", 10),
        data_layer.RecipeIngredient("water", 7),
        data_layer.RecipeIngredient("salt", 1),
    },
)
# Cake
cake_recipe = data_layer.StructuredRecipe(
    "cake",
    recipe_ingredients={
        data_layer.RecipeIngredient("flour", 5),
        data_layer.RecipeIngredient("water", 7),
        data_layer.RecipeIngredient("egg", 2),
        data_layer.RecipeIngredient("sugar", 4),
        data_layer.RecipeIngredient("salt", 1),
    },
)
# Spaghetti
spaghetti_recipe = data_layer.StructuredRecipe(
    "spaghetti",
    recipe_ingredients={
        data_layer.RecipeIngredient("flour", 8),
        data_layer.RecipeIngredient("water", 2),
        data_layer.RecipeIngredient("egg", 5),
        data_layer.RecipeIngredient("salt", 1),
    },
)


def main(argv):
    c.create_recipe(bread_recipe)
    c.create_recipe(cake_recipe)
    c.create_recipe(spaghetti_recipe)


if __name__ == "__main__":
    app.run(main)
