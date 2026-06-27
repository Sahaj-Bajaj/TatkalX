import { useState } from "react";
import StationSelect from "./StationSelect";
import { AvailabilitySkeleton } from "./Skeleton";
import { getAvailability } from "../api/client";

const CLASSES = ["SL", "3A", "2A", "1A"];
const CLASS_LABELS = { SL: "Sleeper", "3A": "AC 3-Tier", "2A": "AC 2-Tier", "1A": "AC 1st Class" };
const todayStr = new Date().toISOString().split("T")[0];

const THEME = {
  HIGH:   { bar: "bg-emerald-500", badge: "bg-emerald-100 text-emerald-700", num: "text-emerald-500", box: "bg-emerald-50 border-emerald-200 text-emerald-800" },
  MEDIUM: { bar: "bg-amber-400",   badge: "bg-amber-100 text-amber-700",   num: "text-amber-500",   box: "bg-amber-50 border-amber-200 text-amber-800"     },
  LOW:    { bar: "bg-red-500",     badge: "bg-red-100 text-red-700",       num: "text-red-500",     box: "bg-red-50 border-red-200 text-red-800"           },
};

const MODEL_FEATURES = [
  ["days_before_journey", "Days until travel — book 30+ days ahead for best odds"],
  ["is_tatkal",           "Tatkal quota — opens 10 AM exactly, 1 day before journey"],
  ["hour_of_booking",     "Booking hour — first minute of Tatkal window is most contested"],
  ["route_popularity",    "Route congestion score (1–5) — busy corridors fill fastest"],
  ["travel_class",        "Class encoding — SL=0 fills fastest, 1A=3 almost always available"],
  ["day_of_week",         "Day of travel — Fri/Sat/Sun reduce availability ~10%"],
  ["month",               "Season — Oct–Jan and May–Jun are peak (festivals + vacations)"],
];

const FEATURE_LABELS = {
  days_before_journey: "Days before journey",
  travel_class:        "Travel class",
  day_of_week:         "Day of week",
  month:               "Month / Season",
  route_popularity:    "Route popularity",
  is_tatkal:           "Tatkal quota",
  hour_of_booking:     "Booking hour",
};

export default function AvailabilityCheck({ stations }) {
  const [source, setSource]     = useState("");
  const [dest, setDest]         = useState("");
  const [date, setDate]         = useState(todayStr);
  const [cls, setCls]           = useState("SL");
  const [isTatkal, setIsTatkal] = useState(false);
  const [result, setResult]     = useState(null);
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);

  async function handleCheck() {
    if (!source || !dest) { setError("Select both stations."); return; }
    const journeyDate = new Date(date);
    const now         = new Date();
    const daysBefore  = Math.max(1, Math.ceil((journeyDate - now) / 86400000));
    if (daysBefore > 120) { setError("IRCTC allows booking up to 120 days in advance."); return; }
    const jsDay     = journeyDate.getDay();
    const dayOfWeek = jsDay === 0 ? 6 : jsDay - 1;
    setError(""); setResult(null); setLoading(true);
    try {
      const data = await getAvailability({
        source, destination: dest, days_before: daysBefore,
        travel_class: cls, day_of_week: dayOfWeek,
        month: journeyDate.getMonth() + 1,
        is_tatkal: isTatkal,
        hour_of_booking: isTatkal ? 10 : new Date().getHours(),
      });
      setResult(data);
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
          Predict Availability
        </h2>

        <div className="grid grid-cols-2 gap-4">
          <StationSelect label="From" value={source} onChange={setSource}
            stations={stations} exclude={dest} />
          <StationSelect label="To"   value={dest}   onChange={setDest}
            stations={stations} exclude={source} />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Journey Date
            </label>
            <input type="date" value={date} min={todayStr}
              onChange={e => setDate(e.target.value)}
              className="border-2 border-slate-200 rounded-xl px-3 py-2.5 text-sm
                         text-slate-700 font-medium focus:outline-none
                         focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-colors" />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Travel Class
            </label>
            <div className="relative">
              <select value={cls} onChange={e => setCls(e.target.value)}
                className="w-full appearance-none border-2 border-slate-200 rounded-xl
                           px-3 pr-8 py-2.5 text-sm text-slate-700 bg-white font-medium
                           focus:outline-none focus:border-indigo-400
                           focus:ring-2 focus:ring-indigo-100 transition-colors cursor-pointer">
                {CLASSES.map(c => <option key={c} value={c}>{c} — {CLASS_LABELS[c]}</option>)}
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2
                              text-slate-400 text-xs">▾</div>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 mt-5">
          <button type="button" role="switch" aria-checked={isTatkal}
            onClick={() => setIsTatkal(v => !v)}
            className={`relative w-10 h-5 rounded-full shrink-0 transition-colors duration-200
                        focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-orange-400 ${
              isTatkal ? "bg-orange-500" : "bg-slate-200"
            }`}>
            <span className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow-sm
                              transition-all duration-200 ${isTatkal ? "left-5" : "left-0.5"}`} />
          </button>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-semibold text-slate-700">Tatkal Quota</span>
            {isTatkal && (
              <span className="text-xs text-orange-500 font-medium">
                Opens 10:00 AM · 1 day before journey
              </span>
            )}
          </div>
        </div>

        {error && (
          <p className="mt-3 text-sm text-red-500 flex items-center gap-1.5">
            <span>⚠</span> {error}
          </p>
        )}

        <button onClick={handleCheck} disabled={loading}
          className="mt-5 w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800
                     disabled:opacity-60 text-white font-semibold py-2.5 rounded-xl
                     text-sm transition-all duration-150 active:scale-[0.99]">
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Predicting…
            </span>
          ) : "Check Availability"}
        </button>

        {!result && !loading && (
          <div className="mt-6 pt-5 border-t border-slate-100">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">
              Model Features (XGBoost · 7 inputs)
            </p>
            <div className="space-y-2">
              {MODEL_FEATURES.map(([feat, desc]) => (
                <div key={feat} className="flex items-start gap-2.5 text-xs">
                  <span className="font-mono text-indigo-500 font-bold shrink-0 pt-px">{feat}</span>
                  <span className="text-slate-400 leading-relaxed">{desc}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {loading && <AvailabilitySkeleton />}

      {result && !loading && (() => {
        const t   = THEME[result.label] ?? THEME.MEDIUM;
        const pct = Math.round(result.availability_probability * 100);
        return (
          <div className="space-y-4 animate-fade-in">
            <div className="bg-white rounded-2xl border border-slate-200 shadow-md p-6">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                    Availability Prediction
                  </p>
                  <p className="text-sm text-slate-600 mt-1 font-medium">
                    <span className="font-mono font-bold text-indigo-700">{result.source}</span>
                    {" → "}
                    <span className="font-mono font-bold text-indigo-700">{result.destination}</span>
                    {" · "}{result.travel_class}
                    {result.is_tatkal && <span className="ml-2 text-orange-500 font-semibold">Tatkal</span>}
                  </p>
                </div>
                <span className={`text-sm font-bold px-3 py-1 rounded-full shrink-0 mt-0.5 ${t.badge}`}>
                  {result.label}
                </span>
              </div>

              <div className="text-center mb-6">
                <div className={`text-6xl font-black tabular-nums leading-none ${t.num}`}>{pct}%</div>
                <p className="text-xs text-slate-400 mt-2 uppercase tracking-widest font-medium">
                  availability probability
                </p>
              </div>

              <div className="w-full bg-slate-100 rounded-full h-2.5 mb-6 overflow-hidden">
                <div className={`${t.bar} h-2.5 rounded-full transition-all duration-700 ease-out`}
                  style={{ width: `${pct}%` }} />
              </div>

              <div className={`rounded-xl border p-4 text-sm leading-relaxed ${t.box}`}>
                💡 {result.recommendation}
              </div>
            </div>

            {result.feature_importance?.top_features?.length > 0 && (
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                    Feature Contributions (SHAP)
                  </p>
                  <p className="text-xs text-slate-300">TreeExplainer · exact values</p>
                </div>
                <div className="space-y-2.5">
                  {(() => {
                    const features = result.feature_importance.top_features;
                    const maxAbs = Math.max(...features.map(f => Math.abs(f.shap_value)), 0.0001);
                    return features.slice(0, 7).map(f => {
                      const pct = (Math.abs(f.shap_value) / maxAbs) * 100;
                      const pos = f.shap_value >= 0;
                      return (
                        <div key={f.feature} className="flex items-center gap-3">
                          <div className="w-36 text-xs text-slate-500 font-medium text-right shrink-0 leading-tight">
                            {FEATURE_LABELS[f.feature] ?? f.feature}
                          </div>
                          <div className="flex-1 h-3.5 bg-slate-50 rounded-full overflow-hidden">
                            <div className={`h-full rounded-full transition-all duration-500 ease-out ${
                              pos ? "bg-emerald-400" : "bg-red-400"
                            }`} style={{ width: `${pct}%` }} />
                          </div>
                          <div className={`w-14 text-xs font-mono font-semibold text-right shrink-0 ${
                            pos ? "text-emerald-600" : "text-red-500"
                          }`}>
                            {pos ? "+" : ""}{f.shap_value.toFixed(3)}
                          </div>
                        </div>
                      );
                    });
                  })()}
                  <p className="text-xs text-slate-300 pt-1">
                    Green = pushes availability up · Red = pushes it down
                  </p>
                </div>
              </div>
            )}
          </div>
        );
      })()}
    </div>
  );
}