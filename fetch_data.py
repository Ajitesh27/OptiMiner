import random
import requests

# NREL_API_KEY = ""

def fetch_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd"}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()['bitcoin']['usd']
    except Exception as e:
        return 100000

def fetch_network_difficulty():
    try:
        url = "https://blockchain.info/q/getdifficulty"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return float(response.text)
    except Exception as e:
        print(f"[WARN] Difficulty fetch failed: {e}")
        return 8.7e13

def estimate_revenue_per_ths(btc_price, difficulty):
    hashes_per_sec = difficulty * (2**32) / 600
    ths_total = hashes_per_sec / 1e12
    btc_per_ths_hour = 37.5 / ths_total
    usd_per_ths_hour = btc_per_ths_hour * btc_price
    return round(usd_per_ths_hour, 4)

def fetch_spot_price(instance_type='g4dn.xlarge', region='us-west-2'):
    return round(random.uniform(0.14, 0.22), 3)

# --- Simulated real-time electricity cost using fixed base + variability ---
def fetch_simulated_realtime_electricity_cost(lat, lon):
    mock_rates = {
        (37.7749, -122.4194): 0.37,  # SF
        (40.7128, -74.0060): 0.15,   # NY
        (31.9686, -99.9018): 0.11,   # TX
    }
    base = mock_rates.get((lat, lon), 0.18)


    # try:
    #     response = requests.get(
    #         "https://developer.nrel.gov/api/utility_rates/v3.json",
    #         params={"api_key": NREL_API_KEY, "lat": lat, "lon": lon},
    #         timeout=5
    #     )
    #     response.raise_for_status()
    #     outputs = response.json().get("outputs", {})
    #     base = float(outputs.get("commercial", base))
    # except Exception as e:
    #     print(f"[WARN] NREL fetch failed for ({lat}, {lon}): {e}")

    # Apply simulated ±20% fluctuation
    variability = random.uniform(0.8, 1.2)
    simulated = round(base * variability, 4)
    return simulated
