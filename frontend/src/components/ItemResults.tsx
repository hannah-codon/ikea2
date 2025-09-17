import { useCallback, useEffect, useState } from "react";
import { ApiHandler, IkeaEntry } from "../apiHandler";
import {
  CodonImageViewer,
  CodonSpinnerView,
} from "@codongit/codon-component-library";
import { IkeaItemCard } from "./basic/IkeaItemCard";
import ItemCarousel from "./basic/ItemCarousel";

export type ItemResultsProps = {
  url: string;
};

export function ItemResults(props: ItemResultsProps) {
  const { url } = props;

  const [item, setItem] = useState<IkeaEntry | null>(null);
  const [similarItems, setSimilarItems] = useState<IkeaEntry[] | null>(null);

  useEffect(() => {
    const fetchItemDetails = async () => {
      const ikeaItem = await ApiHandler.getIkeaEntryFromUrl(url);
      if (ikeaItem !== null) {
        const similar = await ApiHandler.getSimilarIkeaEntries(ikeaItem.pid);
        if (similar !== null) {
          setSimilarItems(similar);
          setItem(ikeaItem);
          return;
        }
      }
      setItem(null);
      setSimilarItems(null);
    };
    fetchItemDetails();
  }, [url]);

  const onExplain = useCallback(() => {
    alert("Explanation feature coming soon!");
  }, []);

  return (
    <div className="flex flex-col h-full w-full items-center justify-center">
      {item === null && (
        <CodonSpinnerView textAbove="Loading item details..." />
      )}
      {item !== null && similarItems !== null && (
        <div className="flex flex-row align-center justify-center items-center">
          <div className="flex flex-col">
            <p>Your item:</p>
            <IkeaItemCard item={item} />
          </div>
          <div className="flex p-8 flex-col gap-2">
            <p>Similar items</p>
            <ItemCarousel items={similarItems} onExplain={onExplain} />
          </div>
        </div>
      )}
    </div>
  );
}
