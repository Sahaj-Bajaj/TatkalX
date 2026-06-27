export function RouteSkeleton() {
  return (
    <div className="space-y-3">
      {[0, 1, 2].map(i => (
        <div key={i} className="bg-white rounded-2xl border border-slate-200 p-5 animate-pulse">
          <div className="flex items-center justify-between mb-3">
            <div className="h-3 w-14 bg-slate-200 rounded" />
            <div className="h-5 w-16 bg-slate-100 rounded-full" />
          </div>
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            {[0, 1, 2].map(j => (
              <span key={j} className="flex items-center gap-2">
                <div className="h-6 w-14 bg-indigo-50 border border-indigo-100 rounded-md" />
                {j < 2 && <div className="w-3 h-2 bg-slate-100 rounded" />}
              </span>
            ))}
          </div>
          <div className="pt-3 border-t border-slate-100 flex gap-5">
            <div className="h-4 w-20 bg-slate-100 rounded" />
            <div className="h-4 w-20 bg-slate-100 rounded" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function AvailabilitySkeleton() {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 animate-pulse space-y-5">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <div className="h-3 w-36 bg-slate-200 rounded" />
          <div className="h-4 w-52 bg-slate-100 rounded" />
        </div>
        <div className="h-7 w-16 bg-slate-100 rounded-full" />
      </div>
      <div className="text-center py-2 space-y-2">
        <div className="h-14 w-28 bg-slate-200 rounded-lg mx-auto" />
        <div className="h-3 w-40 bg-slate-100 rounded mx-auto" />
      </div>
      <div className="h-2.5 w-full bg-slate-100 rounded-full" />
      <div className="h-16 bg-slate-50 rounded-xl" />
    </div>
  );
}