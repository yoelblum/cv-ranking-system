import { Award, ThumbsUp, ThumbsDown, Briefcase, Clock } from "lucide-react";
import type { RankedCandidate } from "../api";

interface ResultsTableProps {
  candidates: RankedCandidate[];
}

function scoreBadge(score: number) {
  if (score >= 80) return "bg-emerald-100 text-emerald-800 border-emerald-200";
  if (score >= 60) return "bg-amber-100 text-amber-800 border-amber-200";
  return "bg-red-100 text-red-800 border-red-200";
}

function rankBadge(rank: number) {
  if (rank === 1) return "bg-yellow-400 text-yellow-900";
  if (rank === 2) return "bg-gray-300 text-gray-800";
  if (rank === 3) return "bg-amber-600 text-white";
  return "bg-gray-200 text-gray-600";
}

export default function ResultsTable({ candidates }: ResultsTableProps) {
  if (candidates.length === 0) return null;

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold flex items-center gap-2">
        <Award className="w-5 h-5 text-amber-600" />
        Top {candidates.length} Ranked Candidates
      </h2>

      <div className="grid gap-4">
        {candidates.map((c, i) => (
          <div
            key={c.id}
            className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow overflow-hidden"
          >
            <div className="flex items-start gap-4 p-5">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shrink-0 ${rankBadge(i + 1)}`}
              >
                #{i + 1}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 flex-wrap">
                  <h3 className="font-semibold text-gray-900">{c.name}</h3>
                  <span
                    className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold ${scoreBadge(c.score)}`}
                  >
                    Score: {c.score}/100
                  </span>
                </div>

                <p className="text-sm text-gray-500 mt-0.5">{c.title}</p>

                <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {c.years_experience} years experience
                  </span>
                </div>

                <div className="flex flex-wrap gap-1.5 mt-2.5">
                  {c.skills.map((skill) => (
                    <span
                      key={skill}
                      className="inline-block rounded-md bg-indigo-50 px-2 py-0.5 text-xs text-indigo-700 font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>

                <div className="mt-3 flex items-start gap-2 text-sm text-gray-600">
                  <Briefcase className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
                  <p>{c.previous_experience}</p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-3">
                  <div className="flex items-start gap-2 text-sm rounded-lg bg-emerald-50 p-3">
                    <ThumbsUp className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                    <span className="text-emerald-800">{c.pros}</span>
                  </div>
                  <div className="flex items-start gap-2 text-sm rounded-lg bg-red-50 p-3">
                    <ThumbsDown className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
                    <span className="text-red-800">{c.cons}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
