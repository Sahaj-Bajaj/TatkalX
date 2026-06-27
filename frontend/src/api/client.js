const BASE =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

async function fetchJson(url, defaultMessage) {
  const res = await fetch(url);

  let data = null;

  try {
    data = await res.json();
  } catch {
    // Response wasn't JSON
  }

  if (!res.ok) {
    throw new Error(
      data?.detail ||
      data?.message ||
      defaultMessage
    );
  }

  return data;
}

export function getStations() {
  return fetchJson(
    `${BASE}/search/stations`,
    "Failed to fetch stations."
  );
}

export function getRoutes(source, destination, maxRoutes = 3) {
  return fetchJson(
    `${BASE}/search/routes?source=${source}&destination=${destination}&max_routes=${maxRoutes}`,
    "Failed to fetch routes."
  );
}

export function getAvailability(params) {
  const query = new URLSearchParams(params).toString();

  return fetchJson(
    `${BASE}/predict/availability?${query}`,
    "Failed to fetch prediction."
  );
}