import { IkeaEntry } from "../../apiHandler";
import { IkeaItemCard } from "./IkeaItemCard";

export type ItemCarouselProps = {
  items: IkeaEntry[];
  onExplain: (item: IkeaEntry) => void;
};

export default function ItemCarousel(props: ItemCarouselProps) {
  const { items, onExplain } = props;
  return (
    <div className="flex flex-col items-center w-80 h-[600px] overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100 border rounded-xl shadow-md bg-white py-4">
      {items.map((item) => (
        <div className="my-2 w-full flex justify-center" key={item.pid}>
          <IkeaItemCard item={item} onExplain={() => onExplain(item)} />
        </div>
      ))}
    </div>
  );
}
