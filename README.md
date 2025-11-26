# Two-Queue System Simulation - Course Project
## COMP 5320/6320 Design and Analysis of Computer Networks

This project implements an event-driven simulation to evaluate the performance of a two-queue system under different packet-assignment strategies. This ReadME was AI generated after the code was complete in order to support less admin work a detailed explanation of the project


## 🚀 Quick Start

### Installation

1. Make sure you have Python 3.7+ installed
2. Install required packages:
   ```bash
   pip install numpy matplotlib
   ```

### Running the Project

**Task 1 - Generate All Plots:**
```bash
python main.py plots
```
This generates 9 plots (3 metrics × 3 parameters) comparing Random and Min-Queue strategies.

**Task 2 - Launch Sensitivity Analysis GUI:**
```bash
python main.py gui
```
This opens an interactive GUI where you can adjust parameters and see results in real-time. This is not a deliverable of the project but used to help visualize the performance metrics and affects with inputs.


## 📊 What This Simulation Does

### System Description
- **Two queues** with independent servers
- Each queue has capacity of **10 packets** (including the one being served)
- **FCFS (First Come First Served)** service policy
- Packets arrive following a **Poisson process**
- Service times are **exponentially distributed**

### Assignment Strategies
1. **Random Selection**: Packets are randomly assigned to either queue
2. **Min-Queue**: Packets go to the queue with the shorter length

### Performance Metrics
1. **Blocking Probability**: Ratio of dropped packets to total offered packets
2. **Average Queue Length**: Average number of packets in a queue (sampled at arrival times)
3. **Average Sojourn Time**: Average time a packet spends in the system

### Parameters Analyzed
1. **Arrival Rate (λ)**: Rate at which packets arrive
2. **Service Rate (μ)**: Rate at which packets are served
3. **Traffic Load (ρ)**: ρ = λ/(2μ)

---

## 🔧 Code Architecture

### 1. `queue_simulation.py` - Core Simulation

**Key Classes:**

**`Packet`**
- Stores packet information (arrival time, ID, queue assignment, service times)

**`Queue`**
- Manages a single queue and its server
- Methods: `enqueue()`, `start_service()`, `finish_service()`

**`Event`**
- Represents arrival or departure events
- Used in priority queue (heap)

**`TwoQueueSimulation`**
- Main simulation engine
- Event-driven architecture:
  - Maintains event queue (priority queue sorted by time)
  - Processes events in chronological order
  - Updates system state at each event
  - Collects statistics

**Key Methods:**
- `run()`: Main simulation loop
- `handle_arrival()`: Process packet arrivals
- `handle_departure()`: Process packet departures
- `select_queue()`: Implement assignment strategy
- `get_metrics()`: Calculate performance metrics

**`run_multiple_simulations()`**
- Runs multiple independent simulations with different seeds
- Averages results for statistical reliability

### 2. `plotting.py` - Generate Plots

**Functions:**
- `plot_vs_arrival_rate()`: Varies λ while keeping μ fixed
- `plot_vs_service_rate()`: Varies μ while keeping λ fixed
- `plot_vs_traffic_load()`: Varies ρ by adjusting λ
- `generate_all_plots()`: Orchestrates all plot generation

### 3. `sensitivity_gui.py` - Interactive GUI

**`SensitivityAnalysisGUI` Class:**
- Built with Tkinter for the interface
- Matplotlib for plotting results
- Threading for non-blocking simulations

**GUI Components:**
- Left panel: Parameter controls
- Right panel: Results visualization (3 subplots)
- Progress indicator

---

## 📈 Understanding the Results

### Expected Behavior

**As Arrival Rate Increases (λ ↑):**
- Blocking probability increases (more packets, same service capacity)
- Queue length increases
- Sojourn time increases

**As Service Rate Increases (μ ↑):**
- Blocking probability decreases (faster service)
- Queue length decreases
- Sojourn time decreases

**As Traffic Load Increases (ρ ↑):**
- All metrics worsen (approaching system capacity)

### Strategy Comparison

**Min-Queue vs Random:**
- Min-Queue typically performs better
- More balanced load distribution
- Lower blocking probability
- Shorter queues
- Reduced sojourn times

**Why Min-Queue is Better:**
- Actively balances load between queues
- Prevents one queue from becoming saturated while the other is idle
- More efficient use of system resources

