from config import *
from fetch_data import *
from agent_rl import QLearningAllocationAgent
from scaler import scale_to_allocation


agent = QLearningAllocationAgent(
    dc_caps={loc: cap for loc, (_, cap) in DATACENTERS.items()},
    max_spot=50
)

def compute_profit(dc_alloc, spot_count, spot_price, revenue_per_ths, elec_costs):
    dc_cost = 0
    total_hash = 0

    for loc, units in dc_alloc.items():
        elec_rate = elec_costs[loc]
        unit_cost = DATACENTER_COST_PER_UNIT + elec_rate * DATACENTER_POWER_KW
        dc_cost += units * unit_cost
        total_hash += units * DATACENTER_HASHRATE_PER_UNIT

    spot_cost = spot_count * spot_price
    total_hash += spot_count * SPOT_HASHRATE_PER_INSTANCE * SPOT_RELIABILITY

    total_cost = dc_cost + spot_cost
    if total_cost > HOURLY_BUDGET:
        return -1 * (total_cost - HOURLY_BUDGET)  # small penalty to encourage exploration
    return total_hash * revenue_per_ths - total_cost

def find_best_allocation():
    btc_price = fetch_btc_price()
    difficulty = fetch_network_difficulty()
    revenue_per_ths = estimate_revenue_per_ths(btc_price, difficulty)
    spot_price = fetch_spot_price()

    elec_costs = {
        loc: fetch_simulated_realtime_electricity_cost(*DATACENTERS[loc][0])
        for loc in DATACENTERS
    }

    raw_allocation = agent.choose_allocation(spot_price, revenue_per_ths)
    smoothed_allocation = agent.clamp_allocation(raw_allocation)

    profit = compute_profit(smoothed_allocation['dc'], smoothed_allocation['spot'], spot_price, revenue_per_ths, elec_costs)
    agent.update(profit, spot_price, revenue_per_ths)
    scale_to_allocation(smoothed_allocation, profit)
    return smoothed_allocation, profit
