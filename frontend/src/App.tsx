import React from "react";
import "@codongit/codon-component-library/styles.css";
import "./index.css";
import { RankChairView } from "./components/RankChairView";

function App() {
  return (
    <div className="flex w-screen h-screen bg-codon-bg-beige">
      <RankChairView />
    </div>
  );
}

export default App;
