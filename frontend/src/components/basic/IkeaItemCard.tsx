import { IkeaEntry } from "../../apiHandler";
import ScoreViewer from "./ScoreViewer";

export type IkeaItemCardProps = {
  item: IkeaEntry;
};

export function IkeaItemCard(props: IkeaItemCardProps) {
  const { item } = props;

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden w-64 h-96 flex flex-col transition-transform transform hover:scale-105 hover:shadow-2xl border border-gray-200">
      <div className="h-3/5 flex items-center justify-center bg-gray-50">
        <img
          src={item.imageUrl}
          alt={item.name}
          className="object-contain h-48 w-full p-4"
        />
      </div>
      <div className="flex flex-col justify-between h-2/5 p-4">
        <h3 className="text-lg font-semibold text-gray-800 truncate mb-2">
          {item.name}
        </h3>
        {item.price && (
          <span className="text-xl font-bold text-green-600">
            ${item.price}
          </span>
        )}
        <ScoreViewer score={item.ecoScore} explanation={item.explanation} />
      </div>
    </div>
  );
}
