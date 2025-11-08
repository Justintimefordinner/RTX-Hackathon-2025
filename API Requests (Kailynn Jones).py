import requests
from datetime import datetime, timedelta, timezone

# --- 1. Define Request Parameters ---
BASE_URL = "https://aeroapi.flightaware.com/aeroapi/"
ENDPOINT = "/airports/KCID/flights/arrivals"  # Correct endpoint

API_KEY  = "SVJxNlzwxckGu3NFhNkCpV7PGwu9og7z"  # Replace with your valid API key

# Cedar Rapids, IA time = Central Daylight Time (UTC-5) on Oct 31, 2025
local_offset = timedelta(hours=-5)

# Local time window: 5:00 PM to 5:10 PM CDT
# Example: 15+ days ago
window_start_local = datetime(2025, 10, 30, 17, 0)  # 5:00 PM CDT
window_end_local   = datetime(2025, 10, 31, 17, 0) # 5:10 PM CDT

# Convert to UTC for API query and format correctly
window_start_utc = (window_start_local - local_offset).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
window_end_utc   = (window_end_local   - local_offset).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Query parameters
QUERY_PARAMS = {
    "start": window_start_utc,
    "end": window_end_utc,
    "max_pages": 1
}

# Headers for authentication using only API key
HEADERS = {
    "Accept": "application/json",
    "x-apikey": API_KEY
}

# --- 2. Make the API Call ---
try:
    response = requests.get(
        f"{BASE_URL}{ENDPOINT}",
        params=QUERY_PARAMS,
        headers=HEADERS  # Authentication using API key only
    )
    response.raise_for_status()
    data = response.json()
    arrivals = data.get("arrivals", [])

    print("✈️ Flights that actually landed at Cedar Rapids (KCID) between 5:00–5:10 PM CDT:")
    print("--------------------------------------------------------------------------------")

    window_start_dt = datetime.strptime(window_start_utc, "%Y-%m-%dT%H:%M:%SZ")
    window_end_dt   = datetime.strptime(window_end_utc, "%Y-%m-%dT%H:%M:%SZ")

    count = 0
    for flight in arrivals:
        if flight.get("cancelled") or flight.get("diverted") or flight.get("position_only"):
            continue

        actual_in = flight.get("actual_in")
        if not actual_in:
            continue

        actual_in_dt = datetime.strptime(actual_in, "%Y-%m-%dT%H:%M:%SZ")

        if window_start_dt <= actual_in_dt <= window_end_dt:
            ident = flight.get("ident", "N/A")
            origin = flight.get("origin", {})
            destination = flight.get("destination", {})

            dep_city = origin.get("city", "N/A")
            dep_iata = origin.get("code_iata", "N/A")
            dep_airport = origin.get("name", "N/A")
            dep_time = flight.get("scheduled_out", "N/A")
            arr_time = actual_in

            print(f"Flight: {ident}")
            print(f"  🛫 From: {dep_city} ({dep_iata}) - {dep_airport}")
            print(f"  🛬 To:   {destination.get('city', 'N/A')} ({destination.get('code_iata', 'N/A')}) - {destination.get('name', 'N/A')}")
            print(f"  ⏰ Departed (scheduled): {dep_time}")
            print(f"  ⏰ Arrived (actual):     {arr_time}")
            print("---------------------------------------------------------")
            count += 1

    if count == 0:
        print("No flights actually landed in that window.")

except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh} | Response: {response.text}")
except requests.exceptions.RequestException as err:
    print(f"Request Error: {err}")
