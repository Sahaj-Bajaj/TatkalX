import { useState, useEffect } from "react";
import RouteSearch from "./components/RouteSearch";
import AvailabilityCheck from "./components/AvailabilityCheck";
import { getStations } from "./api/client";

export default function App() {
  const [tab, setTab]               = useState("routes");
  const [stations, setStations]     = useState({});
  const [stationsLoading, setLoading] = useState(true);

  useEffect(() => {
    getStations()
      .then(setStations)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const tabs = [
    { id: "routes",       label: "Find Routes"         },
    { id: "availability", label: "Check Availability"  },
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-indigo-950 text-white px-6 py-5 shadow-lg">
        <div className="max-w-2xl mx-auto flex items-end justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">TatkalX</h1>
            <p className="text-indigo-400 text-xs mt-0.5">
              Intelligent railway ticket assistant
            </p>
          </div>
          <span className="text-xs bg-orange-500 text-white px-2.5 py-1 rounded-full font-semibold">
            BETA
          </span>
        </div>
      </header>

      {/* Tab bar */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-2xl mx-auto px-6 flex gap-0">
          {tabs.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`px-5 py-3.5 text-sm font-medium border-b-2 -mb-px transition-colors ${
                tab === t.id
                  ? "border-indigo-600 text-indigo-700"
                  : "border-transparent text-slate-500 hover:text-slate-700"
              }`}>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <main className="max-w-2xl mx-auto px-6 py-8">
        {stationsLoading ? (
          <div className="flex items-center gap-2 text-slate-400 text-sm">
            <div className="w-4 h-4 border-2 border-slate-300 border-t-indigo-500
                            rounded-full animate-spin" />
            Loading stations…
          </div>
        ) : tab === "routes" ? (
          <RouteSearch stations={stations} />
        ) : (
          <AvailabilityCheck stations={stations} />
        )}
      </main>
    </div>
  );
}