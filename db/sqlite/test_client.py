import unittest

from db import data_layer
from db.sqlite import client


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.SQLiteClient(":memory:")

    def test_create_and_get_recipe_with_no_ingredients(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)
        actual = self.client.get_recipe(recipe.name)
        self.assertEqual(recipe, actual)

    def test_create_and_get_recipe_with_ingredients(self):
        recipe = data_layer.StructuredRecipe(
            name="cake",
            recipe_ingredients={
                data_layer.RecipeIngredient("flour", 4),
                data_layer.RecipeIngredient("sugar", 3),
                data_layer.RecipeIngredient("salt", 1),
            },
        )
        self.client.create_recipe(recipe)
        actual = self.client.get_recipe("cake")
        self.assertEqual(recipe, actual)

    def test_create_two_recipes_with_same_name(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)
        with self.assertRaises(client.SQLiteException):
            self.client.create_recipe(recipe)

    def test_get_returns_none_if_no_recipe_inserted_yet(self):
        self.assertIsNone(self.client.get_recipe("cake"))
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)
        self.assertIsNone(self.client.get_recipe("cake"))

    def test_get_recipes_with_overlapping_ingredients(self):
        # Bread
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
        self.client.create_recipe(bread_recipe)
        self.client.create_recipe(cake_recipe)
        self.client.create_recipe(spaghetti_recipe)

        self.assertEqual(bread_recipe, self.client.get_recipe("bread"))
        self.assertEqual(cake_recipe, self.client.get_recipe("cake"))
        self.assertEqual(spaghetti_recipe, self.client.get_recipe("spaghetti"))

    def test_update_recipe_with_no_target(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        with self.assertRaises(client.SQLiteException):
            self.client.update_recipe(recipe)

    def test_update_recipe(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)
        updated_recipe = data_layer.StructuredRecipe(
            name="Pascetti",
            recipe_ingredients={data_layer.RecipeIngredient("flour", 4)},
        )
        self.client.update_recipe(updated_recipe)
        self.assertEqual(updated_recipe, self.client.get_recipe("Pascetti"))


if __name__ == "__main__":
    unittest.main()
