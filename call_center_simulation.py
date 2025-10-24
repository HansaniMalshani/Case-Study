import random
import matplotlib.pyplot as plt

# -------------------------------
# Simulation Parameters
# -------------------------------
num_agents_list = [2, 3, 5]  # Different scenarios
arrival_rate = 0.8           # Probability of a call arriving per time step
service_rate = 1.0           # Average service rate per agent
time_steps = 100             # Total simulation time

# Store results for visualization
results = {}

# -------------------------------
# Run simulation for each scenario
# -------------------------------
for num_agents in num_agents_list:
    queue = []
    wait_times = []
    queue_length_over_time = []
    agents_busy = [0] * num_agents  # Track how long each agent is busy

    for t in range(time_steps):
        # New call arrives
        if random.random() < arrival_rate:
            queue.append(0)  # New call with 0 wait time

        # Update agents and queue
        for i in range(num_agents):
            if agents_busy[i] > 0:
                agents_busy[i] -= 1  # Agent finishes call
            elif queue:
                call_wait_time = queue.pop(0)
                wait_times.append(call_wait_time)
                agents_busy[i] = max(1, int(random.expovariate(1/service_rate)) - 1)

        # Increase wait time for calls still in queue
        queue = [x + 1 for x in queue]
        queue_length_over_time.append(len(queue))

    avg_wait = sum(wait_times)/len(wait_times) if wait_times else 0
    results[num_agents] = {
        "avg_wait": avg_wait,
        "queue_length_over_time": queue_length_over_time,
        "calls_left": len(queue)
    }
