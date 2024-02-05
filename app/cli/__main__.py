from db import data_layer
from db.sqlite import client

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('db_path', None, 'Path to the sqlite db file')


def dispatch_action(command, db_path) -> int:
    sql_client = client.SQLiteClient(db_path)
    if command == "create":
        recipe_name = input("Enter the new recipe name: ")

        to_create = data_layer.StructuredRecipe(recipe_name, set())

        while True:
            add_ingredient = input("Add ingredient? [y]/n")
            if add_ingredient == "y":
                ingredient_name = input("Enter name of ingredient: ")
                quantity = input("Enter quantity of ingredient: ")
                if quantity.isdecimal():
                    to_create.recipe_ingredients.add(
                        data_layer.RecipeIngredient(ingredient_name, int(quantity))
                    )
                else:
                    print(f"Quantity {quantity} is not decimal")
                    continue
            elif add_ingredient == "n":
                break
        sql_client.create_recipe(to_create)
    elif command == "get":
        recipe_name = input("Enter recipe to get: ")

        recipe = sql_client.get_recipe(recipe_name)
        if recipe is None:
            print(f"No recipe with name {recipe_name} found")
        else:
            print("\n".join(render_recipe(recipe)))

    return 0


def render_recipe(recipe: data_layer.StructuredRecipe):
    collected = [f"Recipe for {recipe.name}:"]
    for ingredient in recipe.recipe_ingredients:
        collected.append(f" - {ingredient.name}, {ingredient.quantity}")
    return collected


def main(argv):
    args, = argv[1:]
    return dispatch_action(args, FLAGS.db_path)


if __name__ == "__main__":
    app.run(main)
