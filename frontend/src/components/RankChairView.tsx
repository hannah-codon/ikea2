import React, { useState } from "react";
import { UploadItem } from "./UploadItem";
import { IkeaEntry } from "../apiHandler";
import { ItemResults } from "./ItemResults";

export type RankChairProps = {};

export function RankChairView(props: RankChairProps) {
  const [view, setView] = useState<"upload" | "results" | "loading">("upload");
  const [itemUrl, setItemUrl] = useState<string | null>(null);

  const handleUpload = (url: string) => {
    setView("results");
    setItemUrl(url);
  };

  return (
    <div className="flex flex-row h-full w-full items-center justify-center">
      {view === "upload" && <UploadItem onUpload={handleUpload} />}
      {view === "results" && itemUrl && <ItemResults url={itemUrl} />}
    </div>
  );
}
