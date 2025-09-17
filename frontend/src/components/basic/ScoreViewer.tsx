export type ScoreViewerProps = {
  score: number;
  explanation: string;
};

export default function ScoreViewer(props: ScoreViewerProps) {
  const { score, explanation } = props;
  const scoreColors = ["bg-green-500", "bg-yellow-400", "bg-red-500"];

  return (
    <div className="flex flex-col items-center w-full">
      <p className="text-lg font-semibold mb-2">Item Score</p>
      <div className="flex items-center w-40">
        {[0, 1, 2].map((val) => (
          <div
            key={val}
            className={`flex-1 h-4 mx-1 rounded-full transition-all duration-200 ${scoreColors[val]} ${score === val ? "ring-2 ring-black scale-110" : "opacity-60"}`}
            title={val === 0 ? "Good" : val === 1 ? "Average" : "Poor"}
          />
        ))}
      </div>
      <p
        className={`mt-2 text-xl font-bold ${scoreColors[score]} text-white px-4 py-1 rounded-full`}
      >
        {score === 0 ? "Good" : score === 1 ? "Average" : "Poor"} ({score})
      </p>
      <p className="mt-2 text-sm text-gray-700 text-center max-w-xs">
        {explanation}
      </p>
    </div>
  );
}
