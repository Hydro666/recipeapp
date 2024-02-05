"""Model for recipes."""

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String

from db.postgres.models import base

association = Table(
    "recipes_ingredients",
    base.Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
)


class Recipes(base.Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    recipe_name = Column(String(255), nullable=False)

    ingredients = relationship(
        "Ingredients", secondary=association, back_populates="recipes"
    )


class Ingredients(base.Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(255), nullable=False)

    recipes = relationship(
        "Recipes", secondary=association, back_populates="ingredients"
    )
