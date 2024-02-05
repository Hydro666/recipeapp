from db import data_layer
from db.sqlite import client
import argparse

import sys

def dispatch_action(args) -> int:
    sql_client = client.SQLiteClient(args.db_path)
    if args.action == "create":
        recipe_name = input("Enter the new recipe name: ")

        to_create = data_layer.StructuredRecipe(recipe_name, set())

        while True:
            add_ingredient = input("Add ingredient? [y]/n")
            if add_ingredient == "y":
                ingredient_name = input("Enter name of ingredient: ")
                quantity = input("Enter quantity of ingredient: ")
                if quantity.isdecimal():
                    to_create.recipe_ingredients.add(data_layer.RecipeIngredient(ingredient_name, int(quantity)))
                else:
                    print(f"Quantity {quantity} is not decimal")
                    continue
            elif add_ingredient == "n":
                break
        sql_client.create_recipe(to_create)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Front end for recipe app")
    parser.add_argument("action", choices=["create", "get"], type=str)
    parser.add_argument("--db_path", type=str)
    args = parser.parse_args()
    sys.exit(dispatch_action(args))
