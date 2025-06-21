# config.py

# Budget per hour
HOURLY_BUDGET = 10000  # USD

# Datacenter cost model
DATACENTER_COST_PER_UNIT = 1     
DATACENTER_POWER_KW = 1     
DATACENTER_HASHRATE_PER_UNIT = 1000  # TH/s

# Cloud spot instance model
SPOT_HASHRATE_PER_INSTANCE = 100  # TH/s
SPOT_RELIABILITY = 0.85  # Simulate spot unreliability

# Datacenter capacity and location
DATACENTERS = {
    'sf': ((37.7749, -122.4194), 5),
    'ny': ((40.7128, -74.0060), 3),
    'tx': ((31.9686, -99.9018), 8),
}
