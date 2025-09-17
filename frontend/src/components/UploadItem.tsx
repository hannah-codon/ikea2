import React, { useState } from "react";
import {
  CodonButton,
  CodonInput,
  CodonSpinner,
} from "@codongit/codon-component-library";

export type UploadItemProps = { onUpload: (url: string) => void };

export function UploadItem(props: UploadItemProps) {
  const { onUpload } = props;
  const [url, setUrl] = useState<string>("");

  const handleUpload = () => {
    onUpload(url);
  };

  return (
    <div className="flex flex-row gap-2">
      <CodonInput
        type="text"
        placeholder="Paste URL here"
        value={url}
        setValue={setUrl}
      />
      <div className="flex flex-row w-28 items-center justify-center">
        <CodonButton size="small" onClick={handleUpload}>
          Run EcoLens
        </CodonButton>
      </div>
    </div>
  );
}
