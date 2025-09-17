import { CodonStatusCard } from "@codongit/codon-component-library";

export type ScoreViewerProps = {
  score: number;
  explanation: string;
};

export default function ScoreViewer(props: ScoreViewerProps) {
  const { score, explanation } = props;
  const scoreColors = ["bg-green-500", "bg-yellow-400", "bg-red-500"];
  const newScore = Math.min(Math.max(props.score, 0), 2);

  return (
    <div className="flex flex-col items-center w-full h-[200px] justify-center gap-2">
      <div className="flex items-center w-full justify-center">
        <div className="flex w-28">
          {[0, 1, 2].map((val) => (
            <div
              key={val}
              className={`flex-1 h-4 mx-1 rounded-full transition-all duration-200 ${scoreColors[val]} ${newScore === val ? "ring-2 ring-black scale-110" : "opacity-60"}`}
              title={val === 0 ? "Good" : val === 1 ? "Average" : "Poor"}
            />
          ))}
        </div>
        <span className="ml-4 text-gray-700 max-w-xs font-thin text-left text-xs w-[300px]">
          {truncateText(explanation, 200)}
        </span>
      </div>
    </div>
  );
}

const truncateText = (text: string, maxLength: number) => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + "...";
};
