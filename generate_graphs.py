#!/usr/bin/env python3
"""
Generate Performance Visualization Graphs
==========================================
Creates publication-quality graphs from experimental data.

Generates:
1. Bar chart: Execution time comparison
2. Bar chart: Nodes explored comparison
3. Line chart: Algorithm efficiency vs route distance
4. Heatmap: Performance matrix
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


def load_results(filename):
    """Load experimental results from CSV."""
    results = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            for key in row:
                if key != 'algorithm':
                    try:
                        row[key] = float(row[key])
                    except:
                        pass
            results.append(row)
    return results


def plot_execution_time(results, output_file):
    """Generate bar chart for execution time comparison."""
    algorithms = list(set(r['algorithm'] for r in results))
    
    # Group by algorithm
    algo_data = {algo: [] for algo in algorithms}
    for result in results:
        algo_data[result['algorithm']].append(result['time_mean_ms'])
    
    # Calculate averages
    avg_times = {algo: np.mean(times) for algo, times in algo_data.items()}
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(algorithms))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    bars = ax.bar(x, [avg_times[algo] for algo in algorithms], color=colors[:len(algorithms)])
    
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Algorithm Performance Comparison: Execution Time', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Saved: {output_file}")
    plt.close()


def plot_nodes_explored(results, output_file):
    """Generate bar chart for nodes explored comparison."""
    algorithms = list(set(r['algorithm'] for r in results))
    
    # Group by algorithm
    algo_data = {algo: [] for algo in algorithms}
    for result in results:
        algo_data[result['algorithm']].append(result['nodes_explored_mean'])
    
    # Calculate averages
    avg_nodes = {algo: np.mean(nodes) for algo, nodes in algo_data.items()}
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(algorithms))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    bars = ax.bar(x, [avg_nodes[algo] for algo in algorithms], color=colors[:len(algorithms)])
    
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nodes Explored', fontsize=12, fontweight='bold')
    ax.set_title('Algorithm Efficiency: Nodes Explored', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Saved: {output_file}")
    plt.close()


def plot_efficiency_vs_distance(results, output_file):
    """Generate line chart showing efficiency vs route complexity."""
    algorithms = list(set(r['algorithm'] for r in results))
    
    # Group by algorithm and route
    route_lengths = sorted(list(set(r['path_length'] for r in results)))
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    markers = ['o', 's', '^', 'D']
    
    for i, algo in enumerate(algorithms):
        algo_results = [r for r in results if r['algorithm'] == algo]
        
        # Sort by path length
        algo_results_sorted = sorted(algo_results, key=lambda r: r['path_length'])
        
        x_data = [r['path_length'] for r in algo_results_sorted]
        y_data = [r['nodes_explored_mean'] for r in algo_results_sorted]
        
        ax.plot(x_data, y_data, marker=markers[i], color=colors[i], 
                label=algo, linewidth=2, markersize=8)
    
    ax.set_xlabel('Path Length (nodes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nodes Explored', fontsize=12, fontweight='bold')
    ax.set_title('Algorithm Efficiency vs Route Complexity', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Saved: {output_file}")
    plt.close()


def plot_cost_comparison(results, output_file):
    """Generate bar chart for path cost comparison."""
    algorithms = list(set(r['algorithm'] for r in results))
    
    # Group by algorithm
    algo_data = {algo: [] for algo in algorithms}
    for result in results:
        algo_data[result['algorithm']].append(result['cost_mean'])
    
    # Calculate averages
    avg_costs = {algo: np.mean(costs) for algo, costs in algo_data.items()}
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(algorithms))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    bars = ax.bar(x, [avg_costs[algo] for algo in algorithms], color=colors[:len(algorithms)])
    
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Path Cost', fontsize=12, fontweight='bold')
    ax.set_title('Path Cost Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Saved: {output_file}")
    plt.close()


def generate_summary_table(results, output_file):
    """Generate markdown table with results summary."""
    algorithms = list(set(r['algorithm'] for r in results))
    
    # Calculate averages for each algorithm
    summary = {}
    for algo in algorithms:
        algo_results = [r for r in results if r['algorithm'] == algo]
        
        summary[algo] = {
            'time': np.mean([r['time_mean_ms'] for r in algo_results]),
            'nodes': np.mean([r['nodes_explored_mean'] for r in algo_results]),
            'cost': np.mean([r['cost_mean'] for r in algo_results])
        }
    
    # Write markdown table
    with open(output_file, 'w') as f:
        f.write("# Experimental Results Summary\n\n")
        f.write("## Performance Comparison\n\n")
        f.write("| Algorithm | Avg Time (ms) | Avg Nodes Explored | Avg Path Cost |\n")
        f.write("|-----------|---------------|--------------------|--------------|\n")
        
        for algo in algorithms:
            s = summary[algo]
            f.write(f"| {algo} | {s['time']:.3f} | {s['nodes']:.1f} | {s['cost']:.3f} |\n")
        
        f.write("\n## Analysis\n\n")
        
        # Find best in each category
        best_time = min(summary.items(), key=lambda x: x[1]['time'])
        best_nodes = min(summary.items(), key=lambda x: x[1]['nodes'])
        
        f.write(f"- **Fastest Algorithm:** {best_time[0]} ({best_time[1]['time']:.3f} ms)\n")
        f.write(f"- **Most Efficient:** {best_nodes[0]} ({best_nodes[1]['nodes']:.1f} nodes explored)\n")
        
        # Calculate improvements vs baseline
        baseline = summary['Standard Dijkstra']
        f.write("\n### Improvements vs Standard Dijkstra\n\n")
        
        for algo in algorithms:
            if algo == 'Standard Dijkstra':
                continue
            
            s = summary[algo]
            time_improvement = (1 - s['time'] / baseline['time']) * 100
            nodes_improvement = (1 - s['nodes'] / baseline['nodes']) * 100
            
            f.write(f"#### {algo}\n")
            f.write(f"- Time: {time_improvement:+.1f}%\n")
            f.write(f"- Nodes Explored: {nodes_improvement:+.1f}%\n\n")
    
    print(f"Saved: {output_file}")


def main():
    """Generate all graphs."""
    print("\n" + "="*70)
    print("GENERATING PERFORMANCE VISUALIZATION GRAPHS")
    print("="*70 + "\n")
    
    # Check if results exist
    results_file = 'experiments/results/timing_results.csv'
    if not os.path.exists(results_file):
        print(f"ERROR: {results_file} not found")
        print("Run: python experiments/performance_comparison.py first")
        return
    
    # Load results
    results = load_results(results_file)
    print(f"Loaded {len(results)} experimental results\n")
    
    # Generate graphs
    output_dir = 'experiments/results'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating graphs...")
    plot_execution_time(results, f'{output_dir}/execution_time_comparison.png')
    plot_nodes_explored(results, f'{output_dir}/nodes_explored_comparison.png')
    plot_efficiency_vs_distance(results, f'{output_dir}/efficiency_vs_distance.png')
    plot_cost_comparison(results, f'{output_dir}/cost_comparison.png')
    
    print("\nGenerating summary table...")
    generate_summary_table(results, f'{output_dir}/results_summary.md')
    
    print("\n" + "="*70)
    print("GRAPH GENERATION COMPLETE")
    print("="*70)
    print(f"\nGenerated files in {output_dir}/:")
    print("  - execution_time_comparison.png")
    print("  - nodes_explored_comparison.png")
    print("  - efficiency_vs_distance.png")
    print("  - cost_comparison.png")
    print("  - results_summary.md")
    print()


if __name__ == "__main__":
    main()
