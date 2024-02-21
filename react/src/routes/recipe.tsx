import React from 'react';
import { useState } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Table from 'react-bootstrap/Table'
import { useLoaderData } from "react-router-dom";
import RecipeClient from "../external_apis/recipe_client";

const fixedData = {
  "name": "Bread",
  "recipe_ingredients": [
    {"name": "Flour", "quantity": 100},
    {"name": "Water", "quantity": 80},
    {"name": "Salt", "quantity": 2},
    {"name": "yeast", "quantity": 1},
  ]
}

export async function loader({ params }) {
  let c = new RecipeClient("http://localhost:5000");
  const res = await c.getRecipe(params.recipeId);
  return res;
}

function Recipebox({ recipeData }) {
  return (
    <div className="ri-grid">
      <Container>
        <Row>
          <Col>
            <RecipeTitle title={recipeData.name} />
          </Col>
        </Row>
        <Row>
          <Col>
            <IngredientGrid ingredients={recipeData.recipe_ingredients} />
          </Col>
        </Row>
      </Container>
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
      <Table striped bordered hover size="sm">
        <thead>
          {header}
        </thead>
        <tbody>
          {rows}
        </tbody>
      </Table>
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

  const recipe = useLoaderData();

  return (
    <>
      <Recipebox recipeData={recipe} />
    </>
  );
}
