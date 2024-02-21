import React from 'react';
import { useState } from 'react';

const fixedData = {
  "name": "Bread",
  "recipe_ingredients": [
    {"name": "Flour", "quantity": 100},
    {"name": "Water", "quantity": 80},
    {"name": "Salt", "quantity": 2},
    {"name": "yeast", "quantity": 1},
  ]
}

function Recipebox({ recipeData }) {
  return (
    <div className="ri-grid">
      <RecipeTitle title={recipeData.name} />
      <IngredientGrid ingredients={recipeData.recipe_ingredients} />
    </div>
  )
}

function RecipeTitle({ title }) {
  return (
    <h1>{title}</h1>
  )
}

function IngredientGrid( { ingredients }) {
  const header = (
    <>
      <tr>
        <th scope="col">Ingredient name</th>
        <th scope="col">Ingredient quantity</th>
      </tr> 
    </>
  )
  const rows = ingredients.map(ri => <IngredientRow name={ri.name} quantity={ri.quantity} />)
  return (
    <>
      <table>
        <thead>
          {header}
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </>
  )
}

function IngredientRow({ name, quantity }) {
  return (
    <>
      <tr>
        <th>{name}</th>
        <th>{quantity}</th>
      </tr>
    </>
  )
}

export default function Recipe() {
  const [recipeState, setRecipeState] = useState(fixedData);

  return (
    <>
      <Recipebox recipeData={recipeState} />
    </>
  );
}
