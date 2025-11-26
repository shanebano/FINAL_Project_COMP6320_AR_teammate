##AI Used for the following: 
        #formatting code
        #optimizing imports
        #code refactoring
        #documentation
        #code organization
        #code enhancement
        #code debugging
        #code testing
        #plot clean up


###############################  Plotting module for generating performance comparison figures  ###############################

import numpy as np
import matplotlib.pyplot as plt
from queue_simulation import run_multiple_simulations


def plot_vs_arrival_rate(service_rate=1.0, num_runs=10, num_packets=10000, save_prefix=''):
    
    ########################### Generate plots comparing strategies vs arrival rate #############################


    # Range of arrival rates
    arrival_rates = np.linspace(0.2, 1.8, 9)  # λ from 0.2 to 1.8
    
    random_blocking = [] # Blocking probabilities for random strategy
    random_queue_length = [] # Average queue lengths for random strategy
    random_sojourn = [] # Average sojourn times for random strategy
    
    minq_blocking = [] # Blocking probabilities for min-queue strategy
    minq_queue_length = [] # Average queue lengths for min-queue strategy
    minq_sojourn = [] # Average sojourn times for min-queue strategy
    
    print("Simulating vs Arrival Rate...")
    for i, arrival_rate in enumerate(arrival_rates):
        print(f"  Progress: {i+1}/{len(arrival_rates)} (λ={arrival_rate:.2f})")
        
        # Random strategy 
        metrics_random = run_multiple_simulations(
            arrival_rate=arrival_rate, # Lambda
            service_rate=service_rate, # Mu
            strategy='random', # Strategy type
            num_runs=num_runs, # Number of runs
            num_packets=num_packets # Packets per run
        )
        random_blocking.append(metrics_random['blocking_probability']) # Blocking probability
        random_queue_length.append(metrics_random['average_queue_length']) # Average queue length
        random_sojourn.append(metrics_random['average_sojourn_time']) # Average sojourn time
        
        # Min-queue strategy
        metrics_minq = run_multiple_simulations(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            strategy='min_queue',
            num_runs=num_runs,
            num_packets=num_packets
        )
        minq_blocking.append(metrics_minq['blocking_probability'])
        minq_queue_length.append(metrics_minq['average_queue_length'])
        minq_sojourn.append(metrics_minq['average_sojourn_time'])
    
    # Calculate traffic load for x-axis
    traffic_loads = arrival_rates / (2 * service_rate)
    
    # Plot 1: Blocking Probability vs Arrival Rate
    plt.figure(figsize=(10, 6))
    plt.plot(arrival_rates, random_blocking, 'o-', label='Random Selection', linewidth=2)
    plt.plot(arrival_rates, minq_blocking, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Arrival Rate (λ)', fontsize=12)
    plt.ylabel('Blocking Probability', fontsize=12)
    plt.title('Blocking Probability vs Arrival Rate', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}blocking_vs_arrival_rate.png', dpi=300)
    plt.close()
    
    # Plot 2: Average Queue Length vs Arrival Rate
    plt.figure(figsize=(10, 6))
    plt.plot(arrival_rates, random_queue_length, 'o-', label='Random Selection', linewidth=2)
    plt.plot(arrival_rates, minq_queue_length, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Arrival Rate (λ)', fontsize=12)
    plt.ylabel('Average Queue Length', fontsize=12)
    plt.title('Average Queue Length vs Arrival Rate', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}queue_length_vs_arrival_rate.png', dpi=300)
    plt.close()
    
    # Plot 3: Average Sojourn Time vs Arrival Rate
    plt.figure(figsize=(10, 6))
    plt.plot(arrival_rates, random_sojourn, 'o-', label='Random Selection', linewidth=2)
    plt.plot(arrival_rates, minq_sojourn, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Arrival Rate (λ)', fontsize=12)
    plt.ylabel('Average Sojourn Time', fontsize=12)
    plt.title('Average Sojourn Time vs Arrival Rate', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}sojourn_vs_arrival_rate.png', dpi=300)
    plt.close()
    
    print("Plots vs Arrival Rate completed!")


def plot_vs_service_rate(arrival_rate=1.0, num_runs=10, num_packets=10000, save_prefix=''):
    """
    Generate plots comparing strategies vs service rate
    """
    # Range of service rates
    service_rates = np.linspace(0.3, 2.0, 9)  # μ from 0.3 to 2.0
    
    random_blocking = []
    random_queue_length = []
    random_sojourn = []
    
    minq_blocking = []
    minq_queue_length = []
    minq_sojourn = []
    
    print("Simulating vs Service Rate...")
    for i, service_rate in enumerate(service_rates):
        print(f"  Progress: {i+1}/{len(service_rates)} (μ={service_rate:.2f})")
        
        # Random strategy
        metrics_random = run_multiple_simulations(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            strategy='random',
            num_runs=num_runs,
            num_packets=num_packets
        )
        random_blocking.append(metrics_random['blocking_probability'])
        random_queue_length.append(metrics_random['average_queue_length'])
        random_sojourn.append(metrics_random['average_sojourn_time'])
        
        # Min-queue strategy
        metrics_minq = run_multiple_simulations(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            strategy='min_queue',
            num_runs=num_runs,
            num_packets=num_packets
        )
        minq_blocking.append(metrics_minq['blocking_probability'])
        minq_queue_length.append(metrics_minq['average_queue_length'])
        minq_sojourn.append(metrics_minq['average_sojourn_time'])
    
    # Plot 4: Blocking Probability vs Service Rate
    plt.figure(figsize=(10, 6))
    plt.plot(service_rates, random_blocking, 'o-', label='Random Selection', linewidth=2)
    plt.plot(service_rates, minq_blocking, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Service Rate (μ)', fontsize=12)
    plt.ylabel('Blocking Probability', fontsize=12)
    plt.title('Blocking Probability vs Service Rate', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}blocking_vs_service_rate.png', dpi=300)
    plt.close()
    
    # Plot 5: Average Queue Length vs Service Rate
    plt.figure(figsize=(10, 6))
    plt.plot(service_rates, random_queue_length, 'o-', label='Random Selection', linewidth=2)
    plt.plot(service_rates, minq_queue_length, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Service Rate (μ)', fontsize=12)
    plt.ylabel('Average Queue Length', fontsize=12)
    plt.title('Average Queue Length vs Service Rate', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}queue_length_vs_service_rate.png', dpi=300)
    plt.close()
    
    # Plot 6: Average Sojourn Time vs Service Rate
    plt.figure(figsize=(10, 6))
    plt.plot(service_rates, random_sojourn, 'o-', label='Random Selection', linewidth=2)
    plt.plot(service_rates, minq_sojourn, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Service Rate (μ)', fontsize=12)
    plt.ylabel('Average Sojourn Time', fontsize=12)
    plt.title('Average Sojourn Time vs Service Rate', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}sojourn_vs_service_rate.png', dpi=300)
    plt.close()
    
    print("Plots vs Service Rate completed!")


def plot_vs_traffic_load(num_runs=10, num_packets=10000, save_prefix=''):
    """
    Generate plots comparing strategies vs traffic load (ρ = λ/(2μ))
    """
    # Keep μ fixed at 1.0 and vary λ to get different ρ values
    service_rate = 1.0
    traffic_loads = np.linspace(0.1, 0.9, 9)  # ρ from 0.1 to 0.9
    arrival_rates = traffic_loads * 2 * service_rate  # λ = ρ * 2μ
    
    random_blocking = []
    random_queue_length = []
    random_sojourn = []
    
    minq_blocking = []
    minq_queue_length = []
    minq_sojourn = []
    
    print("Simulating vs Traffic Load...")
    for i, (traffic_load, arrival_rate) in enumerate(zip(traffic_loads, arrival_rates)):
        print(f"  Progress: {i+1}/{len(traffic_loads)} (ρ={traffic_load:.2f})")
        
        # Random strategy
        metrics_random = run_multiple_simulations(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            strategy='random',
            num_runs=num_runs,
            num_packets=num_packets
        )
        random_blocking.append(metrics_random['blocking_probability'])
        random_queue_length.append(metrics_random['average_queue_length'])
        random_sojourn.append(metrics_random['average_sojourn_time'])
        
        # Min-queue strategy
        metrics_minq = run_multiple_simulations(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            strategy='min_queue',
            num_runs=num_runs,
            num_packets=num_packets
        )
        minq_blocking.append(metrics_minq['blocking_probability'])
        minq_queue_length.append(metrics_minq['average_queue_length'])
        minq_sojourn.append(metrics_minq['average_sojourn_time'])
    
    # Plot 7: Blocking Probability vs Traffic Load
    plt.figure(figsize=(10, 6))
    plt.plot(traffic_loads, random_blocking, 'o-', label='Random Selection', linewidth=2)
    plt.plot(traffic_loads, minq_blocking, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Traffic Load (ρ = λ/(2μ))', fontsize=12)
    plt.ylabel('Blocking Probability', fontsize=12)
    plt.title('Blocking Probability vs Traffic Load', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}blocking_vs_traffic_load.png', dpi=300)
    plt.close()
    
    # Plot 8: Average Queue Length vs Traffic Load
    plt.figure(figsize=(10, 6))
    plt.plot(traffic_loads, random_queue_length, 'o-', label='Random Selection', linewidth=2)
    plt.plot(traffic_loads, minq_queue_length, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Traffic Load (ρ = λ/(2μ))', fontsize=12)
    plt.ylabel('Average Queue Length', fontsize=12)
    plt.title('Average Queue Length vs Traffic Load', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}queue_length_vs_traffic_load.png', dpi=300)
    plt.close()
    
    # Plot 9: Average Sojourn Time vs Traffic Load
    plt.figure(figsize=(10, 6))
    plt.plot(traffic_loads, random_sojourn, 'o-', label='Random Selection', linewidth=2)
    plt.plot(traffic_loads, minq_sojourn, 's-', label='Min-Queue', linewidth=2)
    plt.xlabel('Traffic Load (ρ = λ/(2μ))', fontsize=12)
    plt.ylabel('Average Sojourn Time', fontsize=12)
    plt.title('Average Sojourn Time vs Traffic Load', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output{save_prefix}sojourn_vs_traffic_load.png', dpi=300)
    plt.close()
    
    print("Plots vs Traffic Load completed!")


def generate_all_plots(num_runs=10, num_packets=10000):
    """
    Generate all 9 required plots for Task 1
    """
    print("="*60)
    print("GENERATING ALL PERFORMANCE PLOTS (TASK 1)")
    print("="*60)
    print(f"Configuration: {num_runs} runs, {num_packets} packets per run\n")
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output', exist_ok=True)
    
    # Generate all plots
    plot_vs_arrival_rate(service_rate=1.0, num_runs=num_runs, num_packets=num_packets)
    print()
    plot_vs_service_rate(arrival_rate=1.0, num_runs=num_runs, num_packets=num_packets)
    print()
    plot_vs_traffic_load(num_runs=num_runs, num_packets=num_packets)
    
    print("\n" + "="*60)
    print("ALL PLOTS COMPLETED!")
    print("Plots saved to /Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output")
    print("="*60)


if __name__ == '__main__':
    # Generate all plots with default settings
    generate_all_plots(num_runs=10, num_packets=10000)
