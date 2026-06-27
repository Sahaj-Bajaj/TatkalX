import { useState, useMemo } from "react";

const W = 720, H = 520, PAD = 52;
const LAT_MIN = 11, LAT_MAX = 30, LON_MIN = 70, LON_MAX = 90;

function geo(lat, lon) {
  const x = PAD + ((lon - LON_MIN) / (LON_MAX - LON_MIN)) * (W - 2 * PAD);
  const y = (H - PAD) - ((lat - LAT_MIN) / (LAT_MAX - LAT_MIN)) * (H - 2 * PAD);
  return { x: Math.round(x * 10) / 10, y: Math.round(y * 10) / 10 };
}

const STATIONS = [
  { code: "NDLS", name: "New Delhi",       lat: 28.64, lon: 77.22 },
  { code: "MMCT", name: "Mumbai Central",  lat: 18.97, lon: 72.82 },
  { code: "HWH",  name: "Howrah",          lat: 22.58, lon: 88.34 },
  { code: "MAS",  name: "Chennai Central", lat: 13.08, lon: 80.27 },
  { code: "SBC",  name: "KSR Bengaluru",   lat: 12.97, lon: 77.57 },
  { code: "SC",   name: "Secunderabad",    lat: 17.44, lon: 78.50 },
  { code: "ADI",  name: "Ahmedabad",       lat: 23.02, lon: 72.57 },
  { code: "JP",   name: "Jaipur",          lat: 26.91, lon: 75.79 },
  { code: "BPL",  name: "Bhopal",          lat: 23.26, lon: 77.41 },
  { code: "NGP",  name: "Nagpur",          lat: 21.15, lon: 79.09 },
  { code: "PUNE", name: "Pune",            lat: 18.52, lon: 73.86 },
  { code: "LKO",  name: "Lucknow",         lat: 26.85, lon: 80.95 },
  { code: "CNB",  name: "Kanpur Central",  lat: 26.45, lon: 80.33 },
  { code: "ALD",  name: "Prayagraj",       lat: 25.44, lon: 81.85 },
  { code: "GWL",  name: "Gwalior",         lat: 26.22, lon: 78.18 },
  { code: "AGC",  name: "Agra Cantt",      lat: 27.18, lon: 78.01 },
  { code: "VSKP", name: "Visakhapatnam",   lat: 17.69, lon: 83.22 },
  { code: "UBL",  name: "Hubballi",        lat: 15.36, lon: 75.12 },
];

const EDGES = [
  ["NDLS","JP"],  ["NDLS","AGC"], ["NDLS","GWL"], ["NDLS","BPL"],
  ["NDLS","CNB"], ["NDLS","LKO"], ["NDLS","HWH"], ["NDLS","MMCT"],
  ["JP","ADI"],   ["JP","BPL"],
  ["AGC","GWL"],  ["AGC","CNB"],
  ["GWL","BPL"],
  ["CNB","LKO"],  ["CNB","ALD"],
  ["LKO","ALD"],
  ["ALD","HWH"],
  ["BPL","NGP"],
  ["NGP","SC"],   ["NGP","HWH"],  ["NGP","PUNE"],
  ["SC","MAS"],   ["SC","SBC"],   ["SC","VSKP"],
  ["SBC","MAS"],  ["SBC","PUNE"], ["SBC","UBL"],
  ["ADI","MMCT"],
  ["MMCT","PUNE"],
  ["PUNE","SC"],
  ["VSKP","HWH"],
  ["UBL","MMCT"],
  ["MAS","HWH"],
];

export default function RailwayGraph({ highlightedPath }) {
  const [tooltip, setTooltip] = useState(null);

  const nodes = useMemo(() => STATIONS.map(s => ({ ...s, ...geo(s.lat, s.lon) })), []);
  const nodeMap = useMemo(() => {
    const m = {};
    nodes.forEach(n => { m[n.code] = n; });
    return m;
  }, [nodes]);

  const pathSet = useMemo(() => new Set(highlightedPath || []), [highlightedPath]);

  function isEdgeOnPath(a, b) {
    if (!highlightedPath || highlightedPath.length < 2) return false;
    for (let i = 0; i < highlightedPath.length - 1; i++) {
      const u = highlightedPath[i], v = highlightedPath[i + 1];
      if ((u === a && v === b) || (u === b && v === a)) return true;
    }
    return false;
  }

  const isEndpoint = code =>
    highlightedPath?.length >= 2 &&
    (code === highlightedPath[0] || code === highlightedPath[highlightedPath.length - 1]);

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 pt-5 pb-3 flex items-start justify-between">
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              Railway Network
            </p>
            <p className="text-sm font-semibold text-slate-700 mt-0.5">
              18 major junctions · Yen's k-shortest paths
            </p>
          </div>
          {highlightedPath?.length >= 2 ? (
            <span className="text-xs font-bold bg-orange-100 text-orange-600
                             px-2.5 py-1 rounded-full mt-0.5 shrink-0">
              Route highlighted
            </span>
          ) : (
            <span className="text-xs text-slate-400 bg-slate-50 border border-slate-200
                             px-2.5 py-1 rounded-full mt-0.5 shrink-0">
              Search a route to highlight
            </span>
          )}
        </div>

        <div className="mx-4 mb-4 rounded-xl overflow-hidden">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full"
            style={{ background: "#0F172A", display: "block" }}>
            <defs>
              <pattern id="rail-dots" x="0" y="0" width="24" height="24"
                patternUnits="userSpaceOnUse">
                <circle cx="1" cy="1" r="0.9" fill="rgba(99,102,241,0.10)" />
              </pattern>
              <filter id="node-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2.5" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>
            <rect width={W} height={H} fill="url(#rail-dots)" />

            {EDGES.map(([a, b]) => {
              const na = nodeMap[a], nb = nodeMap[b];
              if (!na || !nb) return null;
              const on = isEdgeOnPath(a, b);
              return (
                <line key={`e-${a}-${b}`}
                  x1={na.x} y1={na.y} x2={nb.x} y2={nb.y}
                  stroke={on ? "#F97316" : "rgba(99,102,241,0.30)"}
                  strokeWidth={on ? 2.5 : 1.2}
                  strokeDasharray={on ? undefined : "5 4"}
                  strokeLinecap="round" />
              );
            })}

            {EDGES.map(([a, b]) => {
              const na = nodeMap[a], nb = nodeMap[b];
              if (!na || !nb || !isEdgeOnPath(a, b)) return null;
              return (
                <line key={`glow-${a}-${b}`}
                  x1={na.x} y1={na.y} x2={nb.x} y2={nb.y}
                  stroke="#F97316" strokeWidth={9} strokeOpacity={0.16}
                  strokeLinecap="round" />
              );
            })}

            {nodes.map(s => {
              const hl = pathSet.has(s.code);
              const ep = isEndpoint(s.code);
              const r  = ep ? 8 : hl ? 6 : 4.5;
              const fill = ep ? "#F97316" : hl ? "#FB923C" : "#6366F1";
              return (
                <g key={s.code}
                  onMouseEnter={() => setTooltip(s)}
                  onMouseLeave={() => setTooltip(null)}
                  style={{ cursor: "default" }}>
                  <circle cx={s.x} cy={s.y} r={16} fill="transparent" />
                  {hl && (
                    <circle cx={s.x} cy={s.y} r={r + 5} fill="none"
                      stroke={ep ? "#F97316" : "#FB923C"}
                      strokeWidth={1} strokeOpacity={0.4} />
                  )}
                  <circle cx={s.x} cy={s.y} r={r} fill={fill}
                    stroke={hl ? "rgba(255,255,255,0.9)" : "rgba(99,102,241,0.45)"}
                    strokeWidth={hl ? 1.5 : 1}
                    filter={hl ? "url(#node-glow)" : undefined} />
                  <text x={s.x} y={s.y - r - 4} textAnchor="middle"
                    fontSize={hl ? 8.5 : 7.5}
                    fontFamily="ui-monospace,'Courier New',monospace"
                    fontWeight={hl ? "700" : "500"}
                    fill={hl ? "#FFFFFF" : "rgba(255,255,255,0.58)"}
                    letterSpacing="0.06em">
                    {s.code}
                  </text>
                </g>
              );
            })}

            {tooltip && (() => {
              const tw = 118, th = 22;
              const tx = Math.min(Math.max(tooltip.x - tw / 2, 4), W - tw - 4);
              const ty = Math.max(tooltip.y - 38, 4);
              return (
                <g style={{ pointerEvents: "none" }}>
                  <rect x={tx} y={ty} width={tw} height={th} rx={4}
                    fill="rgba(15,23,42,0.94)"
                    stroke="rgba(99,102,241,0.45)" strokeWidth={0.8} />
                  <text x={tx + tw / 2} y={ty + 14} textAnchor="middle"
                    fontSize={9.5} fontWeight="500" fill="#E2E8F0"
                    fontFamily="system-ui,sans-serif">
                    {tooltip.name}
                  </text>
                </g>
              );
            })()}
          </svg>
        </div>

        <div className="flex flex-wrap items-center gap-x-5 gap-y-2 px-5 pb-4 text-xs text-slate-400">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 inline-block" />
            Station node
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-orange-500 inline-block" />
            On selected route
          </span>
          <span className="flex items-center gap-1.5">
            <svg width="20" height="6" className="inline-block">
              <line x1="0" y1="3" x2="20" y2="3"
                stroke="rgba(99,102,241,0.5)" strokeWidth="1.5" strokeDasharray="5 4" />
            </svg>
            Railway link
          </span>
          <span className="ml-auto italic text-slate-300">hover node for full name</span>
        </div>
      </div>

      <div className="bg-indigo-50 border border-indigo-100 rounded-2xl px-5 py-4">
        <p className="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-2">
          Under the hood
        </p>
        <p className="text-sm text-indigo-700 leading-relaxed">
          Nodes are the 18 stations in the NetworkX graph. Edges match{" "}
          <code className="font-mono text-xs bg-indigo-100 px-1 py-0.5 rounded">CONNECTIONS</code>{" "}
          in{" "}
          <code className="font-mono text-xs bg-indigo-100 px-1 py-0.5 rounded">data/stations.py</code>.
          Route search calls{" "}
          <code className="font-mono text-xs bg-indigo-100 px-1 py-0.5 rounded">
            nx.shortest_simple_paths(G, src, dst, weight="weight")
          </code>{" "}
          (Yen's algorithm). The highlighted path flows here via React props from the Find Routes tab.
        </p>
      </div>
    </div>
  );
}