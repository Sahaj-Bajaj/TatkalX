import { useState } from "react";
import StationSelect from "./StationSelect";
import { getAvailability } from "../api/client";

const CLASSES = ["SL", "3A", "2A", "1A"];

const todayStr = new Date().toISOString().split("T")[0];

export default function AvailabilityCheck({ stations }) {
  const [source, setSource]       = useState("");
  const [dest, setDest]           = useState("");
  const [date, setDate]           = useState(todayStr);
  const [cls, setCls]             = useState("SL");
  const [isTatkal, setIsTatkal]   = useState(false);
  const [result, setResult]       = useState(null);
  const [error, setError]         = useState("");
  const [loading, setLoading]     = useState(false);

  async function handleCheck() {
    if (!source || !dest) { setError("Select both stations."); return; }

    const journeyDate = new Date(date);
    const now         = new Date();
    const daysBefore  = Math.max(1, Math.ceil((journeyDate - now) / 86400000));

    if (daysBefore > 120) {
      setError("IRCTC allows booking up to 120 days in advance.");
      return;
    }

    // JS getDay(): 0=Sun…6=Sat → convert to backend: 0=Mon…6=Sun
    const jsDay      = journeyDate.getDay();
    const dayOfWeek  = jsDay === 0 ? 6 : jsDay - 1;

    setError(""); setResult(null); setLoading(true);
    try {
      setResult(await getAvailability({
        source,
        destination:      dest,
        days_before:      daysBefore,
        travel_class:     cls,
        day_of_week:      dayOfWeek,
        month:            journeyDate.getMonth() + 1,
        is_tatkal:        isTatkal,
        hour_of_booking:  isTatkal ? 10 : new Date().getHours(),
      }));
    } catch {
      setError("Cannot reach backend. Is uvicorn running?");
    } finally {
      setLoading(false);
    }
  }

  const theme = {
    HIGH:   { bar: "bg-emerald-500", badge: "bg-emerald-100 text-emerald-700" },
    MEDIUM: { bar: "bg-amber-400",   badge: "bg-amber-100 text-amber-700"   },
    LOW:    { bar: "bg-red-500",     badge: "bg-red-100 text-red-700"       },
  };

  return (
    <div className="space-y-5">
      {/* Form card */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-4">
          Predict Availability
        </h2>

        <div className="grid grid-cols-2 gap-4">
          <StationSelect label="From" value={source} onChange={setSource}
            stations={stations} exclude={dest} />
          <StationSelect label="To"   value={dest}   onChange={setDest}
            stations={stations} exclude={source} />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-slate-600">Journey Date</label>
            <input type="date" value={date} min={todayStr}
              onChange={e => setDate(e.target.value)}
              className="border border-slate-300 rounded-lg px-3 py-2 text-sm
                         focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-slate-600">Class</label>
            <select value={cls} onChange={e => setCls(e.target.value)}
              className="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white
                         focus:outline-none focus:ring-2 focus:ring-indigo-500">
              {CLASSES.map(c => <option key={c}>{c}</option>)}
            </select>
          </div>
        </div>

        {/* Tatkal toggle */}
        <label className="flex items-center gap-3 mt-4 cursor-pointer select-none">
          <input type="checkbox" checked={isTatkal}
            onChange={e => setIsTatkal(e.target.checked)}
            className="w-4 h-4 accent-orange-500" />
          <span className="text-sm font-medium text-slate-700">
            Tatkal Quota
          </span>
          <span className="text-xs text-orange-500">
            Opens 10:00 AM · 1 day before journey
          </span>
        </label>

        {error && <p className="mt-3 text-sm text-red-500">{error}</p>}

        <button onClick={handleCheck} disabled={loading}
          className="mt-5 w-full bg-indigo-600 hover:bg-indigo-700
                     disabled:bg-indigo-300 text-white font-medium py-2.5
                     rounded-xl text-sm transition-colors">
          {loading ? "Predicting…" : "Check Availability"}
        </button>
      </div>

      {/* Result card */}
      {result && (() => {
        const t = theme[result.label];
        const pct = Math.round(result.availability_probability * 100);
        return (
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
            <div className="flex items-center justify-between mb-5">
              <span className="text-sm font-semibold text-slate-700">Availability Prediction</span>
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${t.badge}`}>
                {result.label}
              </span>
            </div>

            {/* Probability bar */}
            <div className="mb-5">
              <div className="flex justify-between text-xs text-slate-400 mb-1.5">
                <span>Probability</span>
                <span className="font-bold text-slate-700 text-sm">{pct}%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2.5">
                <div className={`${t.bar} h-2.5 rounded-full transition-all duration-500`}
                  style={{ width: `${pct}%` }} />
              </div>
            </div>

            {/* Meta */}
            <div className="flex flex-wrap gap-3 text-xs text-slate-400 mb-4">
              <span>{result.source} → {result.destination}</span>
              <span>·</span>
              <span>Class {result.travel_class}</span>
              {result.is_tatkal && (
                <><span>·</span>
                <span className="text-orange-500 font-semibold">Tatkal</span></>
              )}
            </div>

            {/* Recommendation */}
            <p className="text-sm text-slate-600 bg-slate-50 rounded-xl p-4 leading-relaxed">
              💡 {result.recommendation}
            </p>
          </div>
        );
      })()}
    </div>
  );
}