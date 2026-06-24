import { useState } from "react";
import StationSelect from "./StationSelect";
import { getRoutes } from "../api/client";

export default function RouteSearch({ stations }) {
  const [source, setSource]   = useState("");
  const [dest, setDest]       = useState("");
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    if (!source || !dest) { setError("Select both stations."); return; }
    setError(""); setResult(null); setLoading(true);
    try {
      setResult(await getRoutes(source, dest, 3));
    } catch {
      setError("Cannot reach backend. Is uvicorn running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-5">
      {/* Form card */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-4">
          Find Routes
        </h2>
        <div className="grid grid-cols-2 gap-4">
          <StationSelect label="From" value={source} onChange={setSource}
            stations={stations} exclude={dest} />
          <StationSelect label="To"   value={dest}   onChange={setDest}
            stations={stations} exclude={source} />
        </div>

        {error && <p className="mt-3 text-sm text-red-500">{error}</p>}

        <button
          onClick={handleSearch} disabled={loading}
          className="mt-5 w-full bg-indigo-600 hover:bg-indigo-700
                     disabled:bg-indigo-300 text-white font-medium py-2.5
                     rounded-xl text-sm transition-colors"
        >
          {loading ? "Searching…" : "Find Routes"}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-3">
          <p className="text-xs text-slate-400 uppercase tracking-wide font-medium">
            {result.routes_found} route{result.routes_found !== 1 ? "s" : ""} —{" "}
            {result.source.name} to {result.destination.name}
          </p>

          {result.routes.map((route, i) => (
            <div key={i} className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
              {/* Path */}
              <div className="flex items-center gap-2 flex-wrap mb-3">
                {route.path.map((code, j) => (
                  <span key={code} className="flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-indigo-700
                                     bg-indigo-50 px-2 py-0.5 rounded-md">
                      {code}
                    </span>
                    {j < route.path.length - 1 && (
                      <span className="text-slate-300 text-xs">→</span>
                    )}
                  </span>
                ))}
                <span className={`ml-auto text-xs font-semibold px-2.5 py-1 rounded-full ${
                  route.is_direct
                    ? "bg-emerald-100 text-emerald-700"
                    : "bg-amber-100 text-amber-700"
                }`}>
                  {route.is_direct ? "Direct" : `${route.stops} stop${route.stops > 1 ? "s" : ""}`}
                </span>
              </div>

              {/* Stats */}
              <div className="flex gap-5 text-sm text-slate-500">
                <span>🛤 {route.total_distance_km} km</span>
                <span>⏱ {route.total_duration_hrs} hrs</span>
              </div>

              {/* Segments (only for indirect) */}
              {!route.is_direct && (
                <div className="mt-3 pt-3 border-t border-slate-100 space-y-1.5">
                  {route.segments.map((seg, j) => (
                    <div key={j} className="flex justify-between text-xs text-slate-400">
                      <span>{seg.from_name} → {seg.to_name}</span>
                      <span>{seg.distance_km} km · {seg.duration_hrs} hrs</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}