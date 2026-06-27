export default function StationSelect({ label, value, onChange, stations, exclude }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
        {label}
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={e => onChange(e.target.value)}
          className="w-full appearance-none border-2 border-slate-200 rounded-xl
                     px-3 pr-8 py-2.5 text-sm text-slate-700 bg-white font-medium
                     focus:outline-none focus:border-indigo-400 focus:ring-2
                     focus:ring-indigo-100 transition-colors cursor-pointer"
        >
          <option value="">Select station</option>
          {Object.entries(stations)
            .filter(([code]) => code !== exclude)
            .map(([code, info]) => (
              <option key={code} value={code}>
                {info.name} ({code})
              </option>
            ))}
        </select>
        <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2
                        text-slate-400 text-xs">▾</div>
      </div>
    </div>
  );
}