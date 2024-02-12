/// <reference types="vite-plugin-svgr/client" />
import logo from './logo.svg?react';
import './App.css';
import { useState } from 'react';

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

function Recipebox({ recipeData }) {
  const ingredients = recipeData.recipe_ingredients.map(ri => 
    <li key="2">
      {ri.name} : {ri.quantity}
    </li>
  );
  return (
    <>
      <h1>Recipe for: {recipeData.name}</h1>
      <ul>
        {ingredients}
      </ul>
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
        <img src={logo} className="App-logo" alt="logo" />
        <button onClick={oonClick}>Get dat cake</button>
        <Recipebox recipeData={recipeState}/>
      </header>
    </div>
  );
}

export default App;
