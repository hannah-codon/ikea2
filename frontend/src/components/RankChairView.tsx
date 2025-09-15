import React, { useState } from "react";
import { UploadItem } from "./UploadItem";
import { IkeaEntry } from "../apiHandler";

export type RankChairProps = {};

export function RankChairView(props: RankChairProps) {
  const [view, setView] = useState<"upload" | "results">("upload");
  const [ikeaItem, setIkeaItem] = useState<IkeaEntry | null>(null);

  const handleUpload = (url: string) => {
    console.log("Uploading:", url);
    setView("results");
  };

  return (
    <div className="flex flex-row h-full w-full items-center justify-center">
      {view === "upload" && <UploadItem onUpload={handleUpload} />}
      {view === "results" && <div>Results</div>}
    </div>
  );
}
