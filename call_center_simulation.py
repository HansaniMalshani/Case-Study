import random
import queue
import matplotlib.pyplot as plt
import csv
import os

class CallCenterSimulation:
    def __init__(self, servers=3, arrival_rate=1.0, service_rate=0.6, max_time=100):
        self.servers = servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.max_time = max_time
        self.wait_times = []
        self.queue_lengths = []

    def exponential(self, rate):
        return random.expovariate(rate)

    def run(self):
        time = 0
        q = queue.Queue()
        servers_busy = 0
        next_arrival = self.exponential(self.arrival_rate)
        next_departures = []

        while time < self.max_time:
            next_departure = min(next_departures) if next_departures else float("inf")
            next_event = min(next_arrival, next_departure)

            if next_event == float("inf"):
                break
            time = next_event

            if next_arrival <= next_departure:
                # Arrival event
                if servers_busy < self.servers:
                    servers_busy += 1
                    dep_time = time + self.exponential(self.service_rate)
                    next_departures.append(dep_time)
                else:
                    q.put(time)
                next_arrival = time + self.exponential(self.arrival_rate)
            else:
                # Departure event
                next_departures.remove(next_departure)
                servers_busy -= 1
                if not q.empty():
                    arrival_time = q.get()
                    wait = time - arrival_time
                    self.wait_times.append(wait)
                    servers_busy += 1
                    dep_time = time + self.exponential(self.service_rate)
                    next_departures.append(dep_time)
            self.queue_lengths.append(q.qsize())

        avg_wait = sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0
        avg_queue = sum(self.queue_lengths) / len(self.queue_lengths)
        return avg_wait, avg_queue, self.queue_lengths


#  Define scenarios 
scenarios = {
    "Scenario 1: 3 servers, normal load": {"servers": 3, "arrival_rate": 1.0, "service_rate": 0.6},
    "Scenario 2: 5 servers, high load": {"servers": 5, "arrival_rate": 1.2, "service_rate": 0.6},
    "Scenario 3: 3 servers, faster service": {"servers": 3, "arrival_rate": 1.0, "service_rate": 1.0}
}

results = {}
output_dir = "simulation_results"
os.makedirs(output_dir, exist_ok=True)

# Run all scenarios 
for name, params in scenarios.items():
    sim = CallCenterSimulation(**params)
    avg_wait, avg_queue, queue_lengths = sim.run()
    results[name] = {
        "avg_wait": avg_wait,
        "avg_queue": avg_queue,
        "queue_lengths": queue_lengths
    }

    csv_file = os.path.join(output_dir, f"{name.replace(' ', '_')}_queue.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["EventNumber", "QueueLength"])
        for i, q_len in enumerate(queue_lengths, start=1):
            writer.writerow([i, q_len])

    print(f"{name} -> Avg Wait: {avg_wait:.2f}, Avg Queue: {avg_queue:.2f} (CSV saved)")

# Graph 1: Queue Length Over Time 
plt.figure(figsize=(12, 6))
for name, data in results.items():
    plt.plot(data["queue_lengths"], label=name)
plt.title("Queue Length Over Time for Different Scenarios")
plt.xlabel("Event Number")
plt.ylabel("Queue Length")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "queue_length_comparison.png"))
plt.show()

#  Graph 2: Average Wait Time Comparison 
plt.figure(figsize=(8, 5))
avg_waits = [data["avg_wait"] for data in results.values()]
plt.bar(results.keys(), avg_waits, color=["skyblue", "lightgreen", "salmon"])
plt.ylabel("Average Wait Time")
plt.title("Average Wait Time Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "avg_wait_comparison.png"))
plt.show()

# Graph 3: Average Queue Length Comparison 
plt.figure(figsize=(8, 5))
avg_queues = [data["avg_queue"] for data in results.values()]
plt.bar(results.keys(), avg_queues, color=["orange", "lightcoral", "lightseagreen"])
plt.ylabel("Average Queue Length")
plt.title("Average Queue Length Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "avg_queue_comparison.png"))
plt.show()

print("\n✅ 3 graphs saved in the 'simulation_results' folder.")
