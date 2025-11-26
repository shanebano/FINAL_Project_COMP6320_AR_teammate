##AI Generated the start of this file in order to support dynamic input adjustment and performance monitoring.
#Human edited to create sensitivity_gui.py and remove unrelated code/ fix issues 
#this code supported analysis of sensitivity to input parameters.

import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from queue_simulation import TwoQueueSimulation
import random
import heapq


class TwoQueueSimulation:
    """Discrete-event simulation for a two-queue system."""

    def __init__(self, arrival_rate, service_rate, strategy, simulation_time=10000, max_queue_size=10):
        # Initialize the simulation parameters
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.strategy = strategy
        self.simulation_time = simulation_time  # Added simulation_time
        self.max_queue_size = max_queue_size

        # Initialize statistics
        self.current_time = 0.0
        self.total_arrivals = 0
        self.blocked_packets = 0
        self.total_queue_length = [0, 0]  # For both queues
        self.total_sojourn_time = 0
        self.total_served_packets = 0

        # Initialize queues and event list
        self.queues = [0, 0]  # Queue lengths for the two queues
        self.event_queue = []  # Priority queue for events (arrival or departure)

    def select_queue(self):
        """Select which queue to assign a packet to based on the strategy."""
        if self.strategy == "random":
            # Randomly select a queue
            return random.choice([0, 1])
        elif self.strategy == "min-queue":
            # Select the queue with the minimum length
            return 0 if self.queues[0] <= self.queues[1] else 1
        else:
            raise ValueError("Invalid strategy")

    def run(self):
        """Run the simulation and calculate performance metrics."""
        # Schedule the first arrival event
        heapq.heappush(self.event_queue, (random.expovariate(self.arrival_rate), "arrival"))

        # Process events until the simulation time is reached
        while self.event_queue:
            event_time, event_type = heapq.heappop(self.event_queue)
            if event_time > self.simulation_time:
                break
            self.current_time = event_time

            if event_type == "arrival":
                # Handle an arrival event
                self.total_arrivals += 1

                # Select a queue for the packet
                queue_index = self.select_queue()

                if self.queues[queue_index] >= self.max_queue_size:
                    # Packet is blocked
                    self.blocked_packets += 1
                else:
                    # Add the packet to the queue
                    self.queues[queue_index] += 1

                    # Update the total queue length for this queue
                    self.total_queue_length[queue_index] += self.queues[queue_index]

                    # Schedule a departure event for this packet
                    service_time = random.expovariate(self.service_rate)
                    departure_time = self.current_time + service_time
                    heapq.heappush(self.event_queue, (departure_time, f"departure_{queue_index}"))

                # Schedule the next arrival event
                next_arrival_time = self.current_time + random.expovariate(self.arrival_rate)
                heapq.heappush(self.event_queue, (next_arrival_time, "arrival"))

            elif event_type.startswith("departure"):
                # Handle a departure event
                queue_index = int(event_type.split("_")[1])
                if self.queues[queue_index] > 0:
                    self.queues[queue_index] -= 1
                    self.total_served_packets += 1
                    self.total_sojourn_time += self.current_time

        # Calculate performance metrics
        blocking_probability = self.blocked_packets / self.total_arrivals if self.total_arrivals > 0 else 0
        average_queue_length = sum(self.total_queue_length) / self.simulation_time
        average_sojourn_time = self.total_sojourn_time / self.total_served_packets if self.total_served_packets > 0 else 0

        # Return the calculated metrics
        return {
            "blocking_probability": blocking_probability,
            "average_queue_length": average_queue_length,
            "average_sojourn_time": average_sojourn_time,
        }


class DynamicInputGUI:
    """GUI for dynamically adjusting inputs and monitoring performance metrics."""

    def __init__(self, root):
        # Initialize the GUI
        self.root = root
        self.root.title("Dynamic Input GUI for Two-Queue System")

        # Default parameters
        self.arrival_rate = 1.0
        self.service_rate = 1.0

        # Create the plot
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add controls for arrival rate and service rate
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(controls_frame, text="Arrival Rate (λ):").pack(side=tk.LEFT, padx=5)
        self.arrival_rate_slider = tk.Scale(
            controls_frame, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, length=200,
            command=self.update_arrival_rate
        )
        self.arrival_rate_slider.set(self.arrival_rate)
        self.arrival_rate_slider.pack(side=tk.LEFT, padx=5)

        tk.Label(controls_frame, text="Service Rate (μ):").pack(side=tk.LEFT, padx=5)
        self.service_rate_slider = tk.Scale(
            controls_frame, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, length=200,
            command=self.update_service_rate
        )
        self.service_rate_slider.set(self.service_rate)
        self.service_rate_slider.pack(side=tk.LEFT, padx=5)

        # Traffic load display
        self.traffic_load_label = tk.Label(controls_frame, text=f"Traffic Load (ρ): {self.calculate_traffic_load():.2f}")
        self.traffic_load_label.pack(side=tk.LEFT, padx=10)

        # Add buttons
        self.run_button = tk.Button(self.root, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.clear_button = tk.Button(self.root, text="Clear Plot", command=self.clear_plot)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10)

    def calculate_traffic_load(self):
        """Calculate the traffic load ρ = λ / (2μ)."""
        return self.arrival_rate / (2 * self.service_rate) if self.service_rate > 0 else float('inf')

    def update_arrival_rate(self, value):
        """Update the arrival rate from the slider."""
        self.arrival_rate = float(value)
        self.update_traffic_load()

    def update_service_rate(self, value):
        """Update the service rate from the slider."""
        self.service_rate = float(value)
        self.update_traffic_load()

    def update_traffic_load(self):
        """Update the traffic load display."""
        traffic_load = self.calculate_traffic_load()
        self.traffic_load_label.config(text=f"Traffic Load (ρ): {traffic_load:.2f}")

    def run_simulation(self):
        """Run the simulation and update the plot."""
        try:
            # Example data for plotting
            arrival_rates = [i * 0.1 for i in range(1, 11)]
            blocking_probabilities = []
            average_queue_lengths = []
            average_sojourn_times = []

            # Run simulations for each arrival rate
            for arrival_rate in arrival_rates:
                simulation = TwoQueueSimulation(
                    arrival_rate=arrival_rate,
                    service_rate=self.service_rate,
                    strategy="random",  # Change to "min-queue" if needed
                    simulation_time=10000,
                    max_queue_size=10,
                )
                results = simulation.run()
                blocking_probabilities.append(results["blocking_probability"])
                average_queue_lengths.append(results["average_queue_length"])
                average_sojourn_times.append(results["average_sojourn_time"])

            # Update the plot with the results
            self.update_plot(arrival_rates, blocking_probabilities, average_queue_lengths, average_sojourn_times)
        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred while running the simulation: {e}")
            print(f"Error in run_simulation: {e}")

    def update_plot(self, x_data, y1_data, y2_data, y3_data):
        """Update the plot with new data."""
        try:
            self.ax.clear()
            self.ax.plot(x_data, y1_data, label="Blocking Probability", marker='o')
            self.ax.plot(x_data, y2_data, label="Average Queue Length", marker='x')
            self.ax.plot(x_data, y3_data, label="Average Sojourn Time", marker='s')
            self.ax.set_title("Simulation Results")
            self.ax.set_xlabel("Arrival Rate")
            self.ax.set_ylabel("Metrics")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Plot Error", f"An error occurred while updating the plot: {e}")
            print(f"Error in update_plot: {e}")

    def clear_plot(self):
        """Clear the plot."""
        try:
            self.ax.clear()
            self.ax.set_title("Simulation Results")
            self.ax.set_xlabel("Arrival Rate")
            self.ax.set_ylabel("Metrics")
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Clear Plot Error", f"An error occurred while clearing the plot: {e}")
            print(f"Error in clear_plot: {e}")


def main():
    """Entry point for the Dynamic Input GUI."""
    root = tk.Tk()
    app = DynamicInputGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()