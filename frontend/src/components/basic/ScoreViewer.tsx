import { CodonStatusCard } from "@codongit/codon-component-library";

export type ScoreViewerProps = {
  score: number;
  explanation: string;
};

export default function ScoreViewer(props: ScoreViewerProps) {
  const { score, explanation } = props;
  const scoreColors = ["bg-green-500", "bg-yellow-400", "bg-red-500"];
  const statusCardColors = [
    "var(--codon-green-500)",
    "var(--codon-yellow-400)",
    "var(--codon-red-500)",
  ];

  const statusCardColor = statusCardColors[score] || "var(--codon-gray-500)";

  return (
    <div className="flex flex-col items-center w-full gap-2">
      <p className="text-md text-codon-gray-800 font-semibold mb-2">
        Eco score
      </p>
      <div className="flex items-center w-full justify-center">
        <div className="flex w-40">
          {[0, 1, 2].map((val) => (
            <div
              key={val}
              className={`flex-1 h-4 mx-1 rounded-full transition-all duration-200 ${scoreColors[val]} ${score === val ? "ring-2 ring-black scale-110" : "opacity-60"}`}
              title={val === 0 ? "Good" : val === 1 ? "Average" : "Poor"}
            />
          ))}
        </div>
        <span className="ml-3 text-lg font-bold text-gray-800">{score}</span>
        <span className="ml-4 text-sm text-gray-700 max-w-xs text-left">
          {explanation}
        </span>
      </div>
      <CodonStatusCard
        text={score === 0 ? "Good" : score === 1 ? "Average" : "Poor"}
        color={statusCardColor}
        size="small"
      />
    </div>
  );
}
