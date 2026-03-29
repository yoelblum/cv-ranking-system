import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ResultsTable from "./components/ResultsTable";
import { generateCvs, rankCvs, type RankedCandidate } from "./api";
import { AlertCircle, LayoutDashboard, Loader2, CheckCircle2 } from "lucide-react";

export default function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [generating, setGenerating] = useState(false);
  const [ranking, setRanking] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [generateCount, setGenerateCount] = useState<number | null>(null);
  const [results, setResults] = useState<RankedCandidate[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    setGenerating(true);
    setError(null);
    setResults([]);
    setGenerated(false);
    setGenerateCount(null);
    try {
      const res = await generateCvs(jobDescription);
      setGenerated(true);
      setGenerateCount(res.count);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setGenerating(false);
    }
  }

  async function handleRank() {
    setRanking(true);
    setError(null);
    try {
      const ranked = await rankCvs(jobDescription);
      setResults(ranked);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setRanking(false);
    }
  }

  return (
    <div className="flex h-screen">
      <Sidebar
        jobDescription={jobDescription}
        setJobDescription={setJobDescription}
        onGenerate={handleGenerate}
        onRank={handleRank}
        generating={generating}
        ranking={ranking}
        generated={generated}
        generateCount={generateCount}
      />

      <main className="flex-1 overflow-y-auto bg-gray-50 p-8">
        {error && (
          <div className="mb-6 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-800">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {error}
          </div>
        )}

        {generating ? (
          <div className="flex flex-col items-center justify-center h-full">
            <Loader2 className="w-16 h-16 text-indigo-600 animate-spin mb-6" />
            <p className="text-xl font-semibold text-gray-800">
              Generating 600 realistic CVs...
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Running 3 concurrent LLM calls, then multiplying via Faker
            </p>
          </div>
        ) : ranking ? (
          <div className="flex flex-col items-center justify-center h-full">
            <Loader2 className="w-16 h-16 text-amber-600 animate-spin mb-6" />
            <p className="text-xl font-semibold text-gray-800">
              Analyzing & Ranking via RAG...
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Embedding 600 candidates, finding top 5, then evaluating with Gemini
            </p>
          </div>
        ) : results.length > 0 ? (
          <ResultsTable candidates={results} />
        ) : generated ? (
          <div className="flex flex-col items-center justify-center h-full">
            <CheckCircle2 className="w-16 h-16 text-emerald-500 mb-6" />
            <p className="text-xl font-semibold text-gray-800">
              {generateCount} candidates ready
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Click <span className="font-semibold text-amber-600">Rank Candidates</span> to find the top 5 matches
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-gray-400">
            <LayoutDashboard className="w-16 h-16 mb-4 stroke-[1.2]" />
            <p className="text-lg font-medium">No results yet</p>
            <p className="text-sm mt-1">
              Paste a job description, then generate and rank candidates.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
