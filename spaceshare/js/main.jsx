import React from "react";
import { createRoot } from "react-dom/client";
import Index from "./post";

// Create a root
const root = createRoot(document.getElementById("postEntry"));

// This method is only called once
// Insert the post component into the DOM
root.render(<Index url="/api/v1/posts/" />);
