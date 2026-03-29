import { Loader2, Sparkles, Trophy, FileText } from "lucide-react";

interface SidebarProps {
  jobDescription: string;
  setJobDescription: (v: string) => void;
  onGenerate: () => void;
  onRank: () => void;
  generating: boolean;
  ranking: boolean;
  generated: boolean;
  generateCount: number | null;
}

export default function Sidebar({
  jobDescription,
  setJobDescription,
  onGenerate,
  onRank,
  generating,
  ranking,
  generated,
  generateCount,
}: SidebarProps) {
  const busy = generating || ranking;

  return (
    <aside className="w-[340px] shrink-0 border-r border-gray-200 bg-white flex flex-col h-screen">
      <div className="px-5 py-6 border-b border-gray-200">
        <h1 className="text-xl font-bold tracking-tight flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-indigo-600" />
          CV Ranking System
        </h1>
        <p className="text-xs text-gray-500 mt-1">AI-powered candidate evaluation</p>
      </div>

      <div className="flex-1 overflow-y-auto px-5 py-5 space-y-5">
        <div>
          <label className="text-sm font-medium text-gray-700 flex items-center gap-1.5 mb-1.5">
            <FileText className="w-3.5 h-3.5" />
            Job Description
          </label>
          <textarea
            rows={12}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            placeholder="Paste the full job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>

        <div className="space-y-3 pt-2">
          <button
            onClick={onGenerate}
            disabled={busy || !jobDescription.trim()}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {generating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Generating 600 CVs...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Generate Candidates
              </>
            )}
          </button>

          {generateCount !== null && (
            <p className="text-xs text-center text-emerald-600 font-medium">
              {generateCount} candidates generated successfully
            </p>
          )}

          <button
            onClick={onRank}
            disabled={busy || !generated || !jobDescription.trim()}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-amber-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {ranking ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing & Ranking via RAG...
              </>
            ) : (
              <>
                <Trophy className="w-4 h-4" />
                Rank Candidates
              </>
            )}
          </button>
        </div>
      </div>
    </aside>
  );
}
