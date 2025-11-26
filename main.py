#Human generated with AI debugging assistance

import sys
import os


def run_plots():
    #Generate all plots for Task 1
    print("\n" + "="*70)
    print("TASK 1: Generating Performance Comparison Plots")
    print("="*70 + "\n")
    
    from plotting import generate_all_plots
    
    # Create output directory if it doesn't exist
    os.makedirs('/Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output', exist_ok=True)
    
    # Generate all plots
    generate_all_plots(num_runs=10, num_packets=10000)
    
    print("\n✓ Task 1 completed successfully!")
    print("  All plots saved to /Users/shanebano/Documents/GitHub/COMP6320_Final_Project/Output\n")


def run_gui():
    #Launch sensitivity analysis GUI for Task 2
    print("\n" + "="*70)
    print("TASK 2: Launching Sensitivity Analysis GUI")
    print("="*70 + "\n")
    
    from sensitivity_gui import main
    main()


def print_usage():
    #Print usage information
    print("\n" + "="*70)
    print("Two-Queue System Simulation - Course Project")
    print("="*70)
    print("\nUsage:")
    print("  python main.py plots    - Generate all 9 plots for Task 1")
    print("  python main.py gui      - Launch sensitivity analysis GUI for Task 2")
    print("  python main.py all      - Generate plots then launch GUI")
    print("\nDescription:")
    print("  This project simulates a two-queue system comparing Random Selection")
    print("  and Min-Queue packet assignment strategies.")
    print("\n  Task 1: Generates 9 performance plots (3 metrics × 3 parameters)")
    print("  Task 2: Interactive GUI for sensitivity analysis")
    print("="*70 + "\n")


def main():
    #Main entry point
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'plots':
        run_plots()
    elif command == 'gui':
        run_gui()
    elif command == 'all':
        run_plots()
        print("\nPress Enter to continue to GUI...")
        input()
        run_gui()
    elif command in ['help', '-h', '--help']:
        print_usage()
    else:
        print(f"\nError: Unknown command '{command}'")
        print_usage()


if __name__ == '__main__':
    main()
