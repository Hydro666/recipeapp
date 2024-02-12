from absl.testing import absltest
from db import data_layer

"""Function to sort json dictionaries."""


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class DataSerializerTest(absltest.TestCase):
    def _assert_serialized_json_objects_are_equal(self, j1, j2):
        self.assertSameStructure(ordered(j1), ordered(j2))

    def test_should_serialize_structured_recipe_with_ingredients_to_json(self):
        structured_recipe = data_layer.StructuredRecipe(
            "bread",
            {
                data_layer.RecipeIngredient("flour", 100),
                data_layer.RecipeIngredient("water", 80),
                data_layer.RecipeIngredient("salt", 3),
                data_layer.RecipeIngredient("yeast", 1),
            },
        )

        actual = data_layer.DataSerializer().serialize_structured_recipe_to_json(
            structured_recipe
        )

        expected = {
            "name": "bread",
            "recipe_ingredients": [
                {"name": "flour", "quantity": 100},
                {"name": "water", "quantity": 80},
                {"name": "salt", "quantity": 3},
                {"name": "yeast", "quantity": 1},
            ],
        }
        self._assert_serialized_json_objects_are_equal(actual, expected)

    def test_should_serialize_recipe_ingredients_field_of_structured_recipe_with_ingredients_as_json_with_empty_list(
        self,
    ):
        structured_recipe = data_layer.StructuredRecipe("bread", set())

        actual = data_layer.DataSerializer().serialize_structured_recipe_to_json(
            structured_recipe
        )

        expected = {"name": "bread", "recipe_ingredients": []}
        self._assert_serialized_json_objects_are_equal(actual, expected)

    def test_should_parse_valid_json_as_structured_recipe(self):
        json_rep = {
            "name": "bread",
            "recipe_ingredients": [
                {"name": "flour", "quantity": 100},
                {"name": "water", "quantity": 80},
                {"name": "salt", "quantity": 3},
                {"name": "yeast", "quantity": 1},
            ],
        }

        parsed_recipe = data_layer.DataSerializer().parse_json_to_structured_recipe(
            json_rep
        )

        expected = data_layer.StructuredRecipe(
            "bread",
            {
                data_layer.RecipeIngredient("flour", 100),
                data_layer.RecipeIngredient("water", 80),
                data_layer.RecipeIngredient("salt", 3),
                data_layer.RecipeIngredient("yeast", 1),
            },
        )
        self.assertEqual(parsed_recipe, expected)

    def test_should_not_parse_json_with_extra_keys(self):
        json_rep = {
            "junk": "foo",
            "name": "bread",
            "recipe_ingredients": [
                {"name": "flour", "quantity": 100},
                {"name": "water", "quantity": 80},
                {"name": "salt", "quantity": 3},
                {"name": "yeast", "quantity": 1},
            ],
        }

        with self.assertRaises(ValueError):
            data_layer.DataSerializer().parse_json_to_structured_recipe(json_rep)

    def test_should_not_parse_json_with_missing_keys(self):
        json_rep = {
            "recipe_ingredients": [
                {"name": "flour", "quantity": 100},
                {"name": "water", "quantity": 80},
                {"name": "salt", "quantity": 3},
                {"name": "yeast", "quantity": 1},
            ]
        }

        with self.assertRaises(ValueError):
            data_layer.DataSerializer().parse_json_to_structured_recipe(json_rep)

    def test_should_not_parse_json_with_non_list_recipe_ingredients(self):
        json_rep = {
            "name": "bread",
            "recipe_ingredients": str(
                [
                    {"name": "flour", "quantity": 100},
                    {"name": "water", "quantity": 80},
                    {"name": "salt", "quantity": 3},
                    {"name": "yeast", "quantity": 1},
                ]
            ),
        }
        with self.assertRaises(ValueError):
            data_layer.DataSerializer().parse_json_to_structured_recipe(json_rep)


if __name__ == "__main__":
    absltest.main()
