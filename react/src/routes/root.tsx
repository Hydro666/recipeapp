import React from 'react';
import { Link, Outlet, useLoaderData } from "react-router-dom";
import RecipeClient from "../external_apis/recipe_client";

export async function loader() {
  let c = new RecipeClient("http://localhost:5000");
  const res = await c.listRecipes();
  return res;
}

export default function Root() {
  const recipes = useLoaderData();
  return (
    <>
      <h1>This is a recipe app!</h1>
      
      <p>We have recipes:
        <ul>
          {recipes.map((name, i) => ( 
            <li key={i}>
              <Link to={`recipe/${name}`}>
                {name}
              </Link>
            </li>
          ))}
        </ul>

      </p>
      <Outlet />
    </>
  );
}