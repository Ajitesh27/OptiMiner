best_profit_so_far = float('-inf')

def scale_to_allocation(allocation, profit):
    global best_profit_so_far

    if profit > best_profit_so_far:
        best_profit_so_far = profit
        print("NEW BEST STATE FOUND! Notifying AWS to scale up...")
        print(f"   ➤ Profit: ${profit:.2f}")
        print(f"   ➤ Allocation: {allocation}")

        # import boto3
        # ec2 = boto3.client('ec2')
        # ec2.modify_instance_attribute(...)
        # autoscaling = boto3.client('autoscaling')
        # autoscaling.update_auto_scaling_group(...)

