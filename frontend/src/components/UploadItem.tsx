import React, { useState } from "react";
import { CodonButton, CodonInput } from "@codongit/codon-component-library";

export type UploadItemProps = { onUpload: (url: string) => void };

export function UploadItem(props: UploadItemProps) {
  const { onUpload } = props;
  const [url, setUrl] = useState<string>("");

  return (
    <div className="flex flex-row gap-2">
      <CodonInput
        type="text"
        placeholder="Enter IKEA url here"
        value={url}
        setValue={setUrl}
      />
      <CodonButton size="small" onClick={() => onUpload(url)}>
        Run EcoLens
      </CodonButton>
    </div>
  );
}
