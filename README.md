# OptiMiner: Smarter Bitcoin Mining with Cloud Spot Instances and Datacenters  
**MARA Hackathon 2025 (SFO)**

## Overview

**OptiMiner** is an intelligent resource allocator for Bitcoin mining operations. It takes a fixed hourly budget and determines how to split that budget between datacenter hardware and cloud spot instances (like AWS EC2 but upto 90% cheaper since they can be reclaimed by AWS anytime) to maximize mining profitability.

The core idea is simple: use low-cost spot instances when they’re cheap and available, and rely on your own datacenters when cloud prices surge or resources get interrupted. This strategy helps you respond in real time to changing market conditions—whether it's a spike in electricity costs, a rise in Bitcoin difficulty, or a sudden drop in spot availability.

## Why This Project?

Bitcoin mining is no longer about just having the most powerful hardware. It’s about how efficiently you use that hardware—and where. Cloud providers offer discounted, interruptible compute capacity (spot instances), while datacenters provide stability at the cost of higher energy consumption.

OptiMiner helps answer a crucial operational question:

> "Given my current budget and market conditions, where should I invest my compute dollars to mine the most profitably?"

As the market changes, OptiMiner responds accordingly:

- When the price of Bitcoin rises, revenue per terahash increases, so the system ramps up mining.
- If spot prices surge or instances are revoked, OptiMiner leans more heavily on datacenter hardware.
- If mining difficulty increases, OptiMiner reduces spend to preserve profit margins.

## How It Works

Every hour, OptiMiner evaluates the latest available market and system data to decide the optimal allocation of compute resources. Here's the breakdown:

1. **Spot Pricing**  
   Fetches live or near-real-time spot instance prices from AWS.

2. **Datacenter Compute Availability and Cost**  
   Considers how many machines you have, how much they cost to run (based on live electricity prices), and how much hashing power they deliver.

3. **Market Data**  
   Retrieves the current Bitcoin price and network difficulty to estimate mining profitability.

4. **Profit Estimation**  
   Calculates expected revenue per terahash per hour and subtracts operational costs to determine expected profit.

5. **Resource Allocation**  
   Chooses the combination of datacenter units and spot instances that delivers the highest projected profit within the hourly budget.

This process runs continuously, adapting as conditions change.

## What Powers OptiMiner?

- **AWS EC2 Spot Pricing**  
  Uses either real or realistically mocked spot pricing data (g4dn.xlarge-type instances).

- **Real-Time Bitcoin Market Data**  
  Uses public APIs like CoinGecko for Bitcoin price and Blockchain.com for difficulty.

- **Electricity Cost Estimation**  
  Uses base rates per datacenter location and simulates minor fluctuations over time.

- **Reinforcement Learning-Based Agent**  
  A lightweight RL agent continually learns and adapts its allocation strategy based on observed profits.

- **Scaler Integration (Simulated)**  
  When a new optimal allocation is discovered, a simulated call to an AWS scaling agent is triggered.

## Customization and Extensibility

- Add or remove datacenter locations
- Adjust power usage, hardware hashrate, or hourly budget
- Replace mocked APIs with authenticated cloud APIs
- Enable persistent logging or dashboard visualizations
- Modify the reward function to prioritize power efficiency or carbon footprint

