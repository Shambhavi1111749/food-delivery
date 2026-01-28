#!/usr/bin/env python3
"""
Experimental Performance Comparison
====================================
Rigorous experimental evaluation of routing algorithms.

Compares:
1. Standard Dijkstra (baseline)
2. Modified Dijkstra (traffic-aware)
3. A* Search (heuristic-guided)
4. Adaptive Dijkstra (feedback-learning)

Metrics:
- Execution time (ms)
- Nodes explored
- Path cost
- Memory usage

Methodology:
- 100 runs per algorithm per test case
- Statistical analysis (mean, std, median)
- Controlled environment (same graph, same start/end)
- Results saved to CSV for analysis
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import statistics
import csv
from typing import List, Dict, Tuple

from graph.road_graph import RoadGraph
from graph.dijkstra import Dijkstra
from graph.modified_dijkstra import ModifiedDijkstra
from graph.astar import AStar
from graph.adaptive_dijkstra import AdaptiveDijkstra


class PerformanceComparator:
    """
    Experimental framework for algorithm comparison.
    """
    
    def __init__(self, graph: RoadGraph):
        """
        Initialize comparator with road graph.
        
        Args:
            graph: RoadGraph instance
        """
        self.graph = graph
        
        # Initialize algorithms
        self.dijkstra = Dijkstra(graph)
        self.modified_dijkstra = ModifiedDijkstra(graph, vehicle_type='boda')
        self.astar = AStar(graph)
        self.adaptive_dijkstra = AdaptiveDijkstra(graph, vehicle_type='boda')
        
        self.results = []
    
    def run_experiment(self, start: int, end: int, num_runs: int = 100):
        """
        Run experimental comparison.
        
        Args:
            start: Starting node
            end: Ending node
            num_runs: Number of repetitions for statistical significance
        """
        print(f"\n{'='*70}")
        print(f"EXPERIMENTAL COMPARISON: Node {start} → Node {end}")
        print(f"{'='*70}")
        print(f"Runs per algorithm: {num_runs}")
        print(f"Statistical method: Mean ± Std Dev")
        print()
        
        algorithms = [
            ('Standard Dijkstra', self._run_dijkstra),
            ('Modified Dijkstra', self._run_modified_dijkstra),
            ('A* Search', self._run_astar),
            ('Adaptive Dijkstra', self._run_adaptive_dijkstra)
        ]
        
        for algo_name, algo_func in algorithms:
            print(f"Testing: {algo_name}...")
            
            times = []
            nodes_explored = []
            edges_examined = []
            costs = []
            paths = []
            
            for run in range(num_runs):
                # Run algorithm and measure
                start_time = time.perf_counter()
                path, cost, stats = algo_func(start, end)
                end_time = time.perf_counter()
                
                exec_time = (end_time - start_time) * 1000  # Convert to ms
                
                times.append(exec_time)
                nodes_explored.append(stats['nodes_explored'])
                edges_examined.append(stats['edges_examined'])
                costs.append(cost)
                paths.append(path)
            
            # Calculate statistics
            result = {
                'algorithm': algo_name,
                'start_node': start,
                'end_node': end,
                'runs': num_runs,
                'time_mean_ms': statistics.mean(times),
                'time_std_ms': statistics.stdev(times) if len(times) > 1 else 0,
                'time_median_ms': statistics.median(times),
                'time_min_ms': min(times),
                'time_max_ms': max(times),
                'nodes_explored_mean': statistics.mean(nodes_explored),
                'nodes_explored_std': statistics.stdev(nodes_explored) if len(nodes_explored) > 1 else 0,
                'edges_examined_mean': statistics.mean(edges_examined),
                'edges_examined_std': statistics.stdev(edges_examined) if len(edges_examined) > 1 else 0,
                'cost_mean': statistics.mean(costs),
                'cost_std': statistics.stdev(costs) if len(costs) > 1 else 0,
                'path_length': len(paths[0]) if paths[0] else 0
            }
            
            self.results.append(result)
            
            # Print summary
            print(f"  Time: {result['time_mean_ms']:.3f} ± {result['time_std_ms']:.3f} ms")
            print(f"  Nodes explored: {result['nodes_explored_mean']:.1f} ± {result['nodes_explored_std']:.1f}")
            print(f"  Cost: {result['cost_mean']:.3f} ± {result['cost_std']:.3f}")
            print()
    
    def _run_dijkstra(self, start: int, end: int) -> Tuple[List[int], float, Dict]:
        """Run Standard Dijkstra."""
        return self.dijkstra.find_shortest_path(start, end)
    
    def _run_modified_dijkstra(self, start: int, end: int) -> Tuple[List[int], float, Dict]:
        """Run Modified Dijkstra."""
        path, cost, stats = self.modified_dijkstra.find_optimal_path(start, end)
        # Extract base distance
        if 'cost_breakdown' in stats:
            dist = stats['cost_breakdown']['base_distance']
        else:
            dist = cost
        return path, dist, stats
    
    def _run_astar(self, start: int, end: int) -> Tuple[List[int], float, Dict]:
        """Run A* Search."""
        return self.astar.find_shortest_path(start, end)
    
    def _run_adaptive_dijkstra(self, start: int, end: int) -> Tuple[List[int], float, Dict]:
        """Run Adaptive Dijkstra."""
        return self.adaptive_dijkstra.find_optimal_path(start, end)
    
    def save_results(self, filename: str):
        """
        Save results to CSV.
        
        Args:
            filename: Output CSV file
        """
        if not self.results:
            print("No results to save")
            return
        
        fieldnames = self.results[0].keys()
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"Results saved to: {filename}")
    
    def print_comparison_table(self):
        """Print formatted comparison table."""
        if not self.results:
            print("No results to display")
            return
        
        print(f"\n{'='*70}")
        print("PERFORMANCE COMPARISON TABLE")
        print(f"{'='*70}\n")
        
        # Header
        print(f"{'Algorithm':<25} {'Time (ms)':<15} {'Nodes':<10} {'Cost':<10}")
        print(f"{'-'*25} {'-'*15} {'-'*10} {'-'*10}")
        
        # Rows
        for result in self.results:
            algo = result['algorithm']
            time_str = f"{result['time_mean_ms']:.3f} ± {result['time_std_ms']:.2f}"
            nodes_str = f"{result['nodes_explored_mean']:.1f}"
            cost_str = f"{result['cost_mean']:.3f}"
            
            print(f"{algo:<25} {time_str:<15} {nodes_str:<10} {cost_str:<10}")
        
        print(f"\n{'='*70}\n")
        
        # Analysis
        print("ANALYSIS:")
        
        # Find best in each category
        best_time = min(self.results, key=lambda r: r['time_mean_ms'])
        best_nodes = min(self.results, key=lambda r: r['nodes_explored_mean'])
        best_cost = min(self.results, key=lambda r: r['cost_mean'])
        
        print(f"  Fastest: {best_time['algorithm']} ({best_time['time_mean_ms']:.3f} ms)")
        print(f"  Fewest nodes explored: {best_nodes['algorithm']} ({best_nodes['nodes_explored_mean']:.1f} nodes)")
        print(f"  Lowest cost: {best_cost['algorithm']} ({best_cost['cost_mean']:.3f})")
        
        # Calculate improvements
        if len(self.results) >= 2:
            baseline = self.results[0]  # Standard Dijkstra
            
            print(f"\n  Improvements vs Standard Dijkstra:")
            for result in self.results[1:]:
                time_improvement = (1 - result['time_mean_ms'] / baseline['time_mean_ms']) * 100
                nodes_improvement = (1 - result['nodes_explored_mean'] / baseline['nodes_explored_mean']) * 100
                
                print(f"    {result['algorithm']}:")
                print(f"      Time: {time_improvement:+.1f}%")
                print(f"      Nodes: {nodes_improvement:+.1f}%")
        
        print()


def main():
    """Run comprehensive experiments."""
    print("\n" + "="*70)
    print("FOOD DELIVERY SYSTEM - EXPERIMENTAL EVALUATION")
    print("="*70)
    
    # Load graph
    graph = RoadGraph('data/roads.json')
    comparator = PerformanceComparator(graph)
    
    # Test cases (different route lengths)
    test_cases = [
        (0, 1, "Short route"),
        (0, 7, "Medium route"),
        (0, 13, "Long route"),
        (10, 20, "Cross-town route")
    ]
    
    for start, end, description in test_cases:
        print(f"\n{'*'*70}")
        print(f"Test Case: {description} (Node {start} → {end})")
        print(f"{'*'*70}")
        
        comparator.run_experiment(start, end, num_runs=100)
    
    # Save results
    comparator.save_results('experiments/results/timing_results.csv')
    
    # Print final comparison
    comparator.print_comparison_table()
    
    print("\n" + "="*70)
    print("EXPERIMENTAL EVALUATION COMPLETE")
    print("="*70)
    print("\nResults saved to:")
    print("  - experiments/results/timing_results.csv")
    print("\nNext steps:")
    print("  1. Run: python experiments/generate_graphs.py")
    print("  2. View graphs in experiments/results/")
    print()


if __name__ == "__main__":
    main()
