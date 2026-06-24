export default function StationSelect({
  label,
  value,
  onChange,
  stations,
  exclude
}) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-sm font-medium text-slate-600">
        {label}
      </label>

      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white
                   focus:outline-none focus:ring-2 focus:ring-indigo-500"
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
    </div>
  );
}