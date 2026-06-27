import { useState, useEffect, useCallback } from "react";
import RouteSearch from "./components/RouteSearch";
import AvailabilityCheck from "./components/AvailabilityCheck";
import RailwayGraph from "./components/RailwayGraph";
import { getStations } from "./api/client";

const TECH_PILLS = [
  "Railway Network", "Yen's k-Shortest Paths", "XGBoost + SHAP", "Redis Cache", "PostgreSQL",
];

export default function App() {
  const [tab, setTab]                         = useState("routes");
  const [stations, setStations]               = useState({});
  const [stationsLoading, setLoading]         = useState(true);
  const [highlightedPath, setHighlightedPath] = useState(null);
  const [apiStatus, setApiStatus]             = useState("checking");

  useEffect(() => {
    getStations()
      .then(data => { setStations(data); setApiStatus("ok"); })
      .catch(() => setApiStatus("error"))
      .finally(() => setLoading(false));
  }, []);

  const handleRouteFound = useCallback(path => setHighlightedPath(path), []);

  const tabs = [
    { id: "routes",       label: "Find Routes",  icon: "🛤" },
    { id: "availability", label: "Availability", icon: "🎫" },
    { id: "network",      label: "Network Map",  icon: "🗺" },
  ];

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-gradient-to-br from-blue-950 via-indigo-950 to-slate-900 text-white">
        <div className="max-w-3xl mx-auto px-6 py-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-3xl font-black tracking-tight leading-none">
                  Tatkal<span className="text-orange-400">X</span>
                </h1>
                <span className="text-xs bg-orange-500 text-white px-2 py-0.5 rounded
                                 font-bold tracking-wide self-center">BETA</span>
              </div>
              <p className="text-indigo-300/75 text-sm mt-1.5">
                Intelligent Railway Ticket Assistant
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs text-indigo-300/70
                            bg-white/5 border border-white/10 px-3 py-1.5 rounded-full shrink-0">
              <span className={`w-1.5 h-1.5 rounded-full inline-block ${
                apiStatus === "ok"    ? "bg-emerald-400 animate-pulse" :
                apiStatus === "error" ? "bg-red-400" :
                                        "bg-amber-400 animate-pulse"
              }`} />
              {apiStatus === "ok" ? "API Online" :
               apiStatus === "error" ? "API Offline" : "Connecting…"}
            </div>
          </div>
          <div className="flex flex-wrap gap-1.5 mt-4">
            {TECH_PILLS.map(p => (
              <span key={p} className="text-xs text-indigo-200/65 bg-white/5
                                       border border-white/10 px-2.5 py-0.5 rounded-full">
                {p}
              </span>
            ))}
          </div>
        </div>
      </header>

      <div className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-6 flex">
          {tabs.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`flex items-center gap-2 px-5 py-3.5 text-sm font-medium
                          border-b-2 -mb-px transition-all duration-150 ${
                tab === t.id
                  ? "border-indigo-600 text-indigo-700"
                  : "border-transparent text-slate-500 hover:text-slate-700"
              }`}>
              <span>{t.icon}</span>
              <span>{t.label}</span>
            </button>
          ))}
        </div>
      </div>

      <main className="max-w-3xl mx-auto px-6 py-8">
        {stationsLoading ? (
          <div className="animate-pulse space-y-4">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 h-40" />
          </div>
        ) : tab === "routes" ? (
          <RouteSearch stations={stations} onRouteFound={handleRouteFound} />
        ) : tab === "availability" ? (
          <AvailabilityCheck stations={stations} />
        ) : (
          <RailwayGraph highlightedPath={highlightedPath} />
        )}
      </main>
    </div>
  );
}