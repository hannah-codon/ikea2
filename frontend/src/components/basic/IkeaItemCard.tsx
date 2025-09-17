import { CodonButton } from "@codongit/codon-component-library";
import { IkeaEntry } from "../../apiHandler";
import ScoreViewer from "./ScoreViewer";

export type IkeaItemCardProps = {
  item: IkeaEntry;
  onExplain?: () => void;
};

export function IkeaItemCard(props: IkeaItemCardProps) {
  const { item, onExplain } = props;

  const secondDivHeight = onExplain ? "h-[300px]" : "h-[200px]";

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden w-64 flex flex-col transition-transform transform hover:shadow-xl border border-gray-200">
      <div className="flex flex-col h-[250px]">
        <h3 className="text-lg font-semibold text-codon-gray-800 truncate mb-2 px-4 pt-4 text-center">
          {item.name}
        </h3>
        <div className="flex flex-1 items-center justify-center">
          <img
            src={item.imageUrl}
            alt={item.name}
            className="object-contain h-40 w-full p-4"
          />
        </div>
      </div>
      <div className={`flex flex-col justify-between p-4 ${secondDivHeight}`}>
        {item.price && (
          <span className="text-xl font-bold text-codon-gray-600">
            {item.price} SEK
          </span>
        )}
        <ScoreViewer score={item.ecoScore} explanation={item.explanation} />
        {onExplain && <CodonButton onClick={onExplain}>Explain</CodonButton>}
      </div>
    </div>
  );
}
