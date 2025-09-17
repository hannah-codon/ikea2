import React from "react";
import "@codongit/codon-component-library/styles.css";
import "./index.css";
import { RankChairView } from "./components/RankChairView";
import { CodonModalProvider } from "@codongit/codon-component-library";

function App() {
  return (
    <CodonModalProvider>
      <div className="flex w-screen h-screen bg-codon-bg-beige">
        <RankChairView />
      </div>
    </CodonModalProvider>
  );
}

export default App;
