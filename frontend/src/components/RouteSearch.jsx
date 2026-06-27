import { useState } from "react";
import StationSelect from "./StationSelect";
import { RouteSkeleton } from "./Skeleton";
import { getRoutes } from "../api/client";

export default function RouteSearch({ stations, onRouteFound }) {
  const [source, setSource]   = useState("");
  const [dest, setDest]       = useState("");
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    if (!source || !dest) { setError("Select both stations."); return; }
    setError(""); setResult(null); setLoading(true);
    try {
      const data = await getRoutes(source, dest, 3);
      setResult(data);
      if (data.routes?.[0]?.path) onRouteFound?.(data.routes[0].path);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-5">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-5">
          Find Routes
        </h2>
        <div className="grid grid-cols-2 gap-4">
          <StationSelect label="From" value={source} onChange={setSource}
            stations={stations} exclude={dest} />
          <StationSelect label="To"   value={dest}   onChange={setDest}
            stations={stations} exclude={source} />
        </div>

        {error && (
          <p className="mt-3 text-sm text-red-500 flex items-center gap-1.5">
            <span>⚠</span> {error}
          </p>
        )}

        <button onClick={handleSearch} disabled={loading}
          className="mt-5 w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800
                     disabled:opacity-60 text-white font-semibold py-2.5 rounded-xl
                     text-sm transition-all duration-150 active:scale-[0.99]">
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white
                               rounded-full animate-spin" />
              Searching…
            </span>
          ) : "Find Routes"}
        </button>

        {!result && !loading && (
          <div className="mt-6 pt-5 border-t border-slate-100">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">
              How it works
            </p>
            <ol className="space-y-2.5">
              {[
                ["Yen's k-shortest paths", "Finds up to 3 alternatives — because the shortest route may have no availability."],
                ["Weighted graph edges",   "Each edge carries real distance (km) and duration (hrs)."],
                ["Redis cache",            "Results cached for 1 hour. ⚡ badge appears on cache hits."],
                ["Network Map tab",        "Click any route card to highlight its path on the geographic map."],
              ].map(([title, desc]) => (
                <li key={title} className="flex gap-3 text-sm">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                  <span>
                    <span className="font-semibold text-slate-600">{title} — </span>
                    <span className="text-slate-400">{desc}</span>
                  </span>
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>

      {loading && <RouteSkeleton />}

      {result && !loading && (
        <div className="space-y-3 animate-fade-in">
          <div className="flex items-center justify-between px-1">
            <p className="text-xs text-slate-400 uppercase tracking-wide font-medium">
              {result.routes_found} route{result.routes_found !== 1 ? "s" : ""} —{" "}
              {result.source?.name || source} → {result.destination?.name || dest}
            </p>
            {result.from_cache && (
              <span className="flex items-center gap-1 text-xs font-semibold text-emerald-600
                               bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
                ⚡ Cached
              </span>
            )}
          </div>

          {result.routes.map((route, i) => (
            <RouteCard key={i} route={route} index={i}
              onClick={() => onRouteFound?.(route.path)} />
          ))}
        </div>
      )}
    </div>
  );
}

function RouteCard({ route, index, onClick }) {
  return (
    <div onClick={onClick}
      className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5
                 hover:border-indigo-300 hover:shadow-md cursor-pointer group
                 transition-all duration-200 active:scale-[0.995]">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
          Route {index + 1}
        </span>
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
          route.is_direct
            ? "bg-emerald-100 text-emerald-700"
            : "bg-amber-100 text-amber-700"
        }`}>
          {route.is_direct ? "Direct" : `${route.stops} stop${route.stops > 1 ? "s" : ""}`}
        </span>
      </div>

      <div className="flex items-center gap-1.5 flex-wrap mb-4">
        {route.path.map((code, j) => (
          <span key={code} className="flex items-center gap-1.5">
            <span className="font-mono text-sm font-bold text-indigo-700
                             bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md
                             group-hover:bg-indigo-100 transition-colors">
              {code}
            </span>
            {j < route.path.length - 1 && (
              <svg width="12" height="8" viewBox="0 0 12 8" fill="none"
                className="text-slate-300 shrink-0">
                <path d="M1 4h10M8 1l3 3-3 3" stroke="currentColor"
                  strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            )}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-4 text-sm text-slate-500
                      pt-3 border-t border-slate-100">
        <span className="flex items-center gap-1.5">
          <span className="text-xs">🛤</span>
          <span className="font-semibold text-slate-700">{route.total_distance_km}</span>
          <span className="text-slate-400 text-xs">km</span>
        </span>
        <span className="flex items-center gap-1.5">
          <span className="text-xs">⏱</span>
          <span className="font-semibold text-slate-700">{route.total_duration_hrs}</span>
          <span className="text-slate-400 text-xs">hrs</span>
        </span>
        <span className="ml-auto text-xs text-indigo-400 font-medium
                         opacity-0 group-hover:opacity-100 transition-opacity">
          View on map →
        </span>
      </div>

      {!route.is_direct && (
        <div className="mt-3 pt-3 border-t border-slate-100 space-y-1.5">
          {route.segments.map((seg, j) => (
            <div key={j} className="flex justify-between text-xs text-slate-400">
              <span>{seg.from_name} → {seg.to_name}</span>
              <span className="font-mono">{seg.distance_km} km · {seg.duration_hrs} hrs</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}