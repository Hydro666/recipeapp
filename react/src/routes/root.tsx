import React from 'react';
import { Outlet } from "react-router-dom";

export default function Root() {
  return (
    <>
      <h1>This is a recipe app!</h1>
      <Outlet />
    </>
  );
}