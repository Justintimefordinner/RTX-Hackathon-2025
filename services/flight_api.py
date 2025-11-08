import requests
from datetime import datetime, timedelta, timezone
from config import API_KEY, BASE_URL

def get_flights(arrival_airport="KCID", start_local=None, end_local=None):
    """
    Fetch historical flights arriving at a given airport in a time window.
    """
    # Default time window if not provided
    if not start_local or not end_local:
        start_local = datetime.utcnow() - timedelta(days=30)
        end_local = datetime.utcnow()

    # Convert local to UTC
    local_offset = timedelta(hours=-5)
    start_utc = (start_local - local_offset).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_utc   = (end_local   - local_offset).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    endpoint = f"airports/{arrival_airport}/flights/arrivals"
    headers = {
        "Accept": "application/json",
        "x-apikey": API_KEY
    }
    params = {
        "start": start_utc,
        "end": end_utc,
        "max_pages": 1
    }

    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("arrivals", [])
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return []
