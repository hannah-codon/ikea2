import React, { useState } from "react";
import { UploadItem } from "./UploadItem";
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
      {view === "upload" && (
        <div className="flex flex-col gap-10 items-center">
          <div className="flex flex-col gap-4 items-center">
            <p className="text-xl font-bold">IKEA EcoLens</p>
            <p className="text-lg w-[500px] text-center">
              EcoLens is an AI-powered advisor that helps shoppers understand
              the sustainability of their furniture choices.
            </p>
          </div>
          <UploadItem onUpload={handleUpload} />
        </div>
      )}
      {view === "results" && itemUrl && <ItemResults url={itemUrl} />}
    </div>
  );
}
