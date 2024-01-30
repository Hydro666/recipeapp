from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import recipe

engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/testytest', echo=True)

Session = sessionmaker(engine)

def bootstrap():
    recipe.Recipes.metadata.create_all(engine)

def fill_with_dummy():
    with Session() as session:
        print('Doing')
        ings = [
            recipe.Ingredients(ingredient_name='flour'),
            recipe.Ingredients(ingredient_name='water'),
            recipe.Ingredients(ingredient_name='salt'),
            recipe.Ingredients(ingredient_name='yeast'),
        ]
        resps = [
            recipe.Recipes(recipe_name='pain de capagne', ingredients=ings)
        ]
        session.add_all(ings)
        session.add_all(resps)
        session.commit()


if __name__ == '__main__':
    fill_with_dummy()
