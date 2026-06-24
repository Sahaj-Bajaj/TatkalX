const BASE =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

export async function getStations() {
  const res = await fetch(`${BASE}/search/stations`);

  if (!res.ok) {
    throw new Error("Failed to fetch stations");
  }

  return res.json();
}

export async function getRoutes(source, destination, maxRoutes = 3) {
  const res = await fetch(
    `${BASE}/search/routes?source=${source}&destination=${destination}&max_routes=${maxRoutes}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch routes");
  }

  return res.json();
}

export async function getAvailability(params) {
  const query = new URLSearchParams(params).toString();

  const res = await fetch(
    `${BASE}/predict/availability?${query}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch prediction");
  }

  return res.json();
}