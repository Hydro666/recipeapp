/// <reference types="vite-plugin-svgr/client" />
import './App.css';
import { useState } from 'react';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const baseUrl = "http://localhost:5000"


const fixedData = {
  "name": "Bread",
  "recipe_ingredients": [
    {"name": "Flour", "quantity": 100},
    {"name": "Water", "quantity": 80},
    {"name": "Salt", "quantity": 2},
    {"name": "yeast", "quantity": 1},
  ]
}

function RecipeSelector({ choices }) {

}

function Recipebox({ recipeData }) {
  return (
    <>
      <RecipeTitle title={recipeData.name} />
      <IngredientGrid ingredients={recipeData.recipe_ingredients} />
    </>
  )
}

function RecipeTitle({ title }) {
  return (
    <h1>{title}</h1>
  )
}

function IngredientGrid( { ingredients }) {
  const rows = ingredients.map(ri => {
    return <IngredientRow name={ri.name} quantity={ri.quantity} />
  })
  const header = (
    <>
      <tr>
        <th scope="col">Ingredient name</th>
        <th scope="col">Ingredient quantity</th>
      </tr> 
    </>
  )
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

function App() {
  const [recipeState, setRecipeState] = useState(fixedData);

  async function oonClick(e) {
    const response = await fetch(baseUrl + "/recipe/cake");
    const json = await response.json();
    setRecipeState(json);
  }

  return (
    <div className="App">
      <header className="App-header">
        <Recipebox recipeData={recipeState} />
      </header>
    </div>
  );
}

export default App;
