import React from "react";
import { CodonButton } from "@codongit/codon-component-library";
import "@codongit/codon-component-library/styles.css";
import "./index.css";

function App() {
  return (
    <>
      <CodonButton onClick={() => console.log("click")}>Click me</CodonButton>
    </>
  );
}

export default App;
