import time
import sys
from optimizer import find_best_allocation
from scaler import scale_to_allocation

def run_continuous_loop(interval_minutes=1):
    step_count = 0
    while True:
        step_count += 1
        allocation, profit = find_best_allocation()

        spot = allocation['spot']
        sf = allocation['dc'].get('sf', 0)
        ny = allocation['dc'].get('ny', 0)
        tx = allocation['dc'].get('tx', 0)

        sys.stdout.write('\r' + ' ' * 100 + '\r')

        scale_to_allocation(allocation, profit)

        sys.stdout.write(
            f"\rStep {step_count:04d} | Profit: ${profit:7.2f} | Spot Instances: {spot:3d} | DCs: SF={sf} NY={ny} TX={tx}      "
        )
        sys.stdout.flush()

        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    run_continuous_loop(interval_minutes=0.01)
