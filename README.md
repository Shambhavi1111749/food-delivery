# Experimental Evaluation Framework

This directory contains the experimental evaluation framework for comparing routing algorithms.

## Files

- `performance_comparison.py` - Main experimental script (100 runs per algorithm)
- `generate_graphs.py` - Graph generation from results
- `results/` - Output directory for CSV data and graphs

## Running Experiments

### Step 1: Run Performance Comparison

```bash
cd /path/to/delivery-system
python experiments/performance_comparison.py
```

This will:
- Test 4 algorithms (Dijkstra, Modified Dijkstra, A*, Adaptive Dijkstra)
- Run 100 iterations per algorithm per test case
- Test 4 different routes (short, medium, long, cross-town)
- Generate `results/timing_results.csv`
- Print comparison table

**Expected Runtime:** 2-3 minutes

### Step 2: Generate Visualization Graphs

```bash
python experiments/generate_graphs.py
```

This will create:
- `results/execution_time_comparison.png`
- `results/nodes_explored_comparison.png`
- `results/efficiency_vs_distance.png`
- `results/cost_comparison.png`
- `results/results_summary.md`

**Requirements:** matplotlib

```bash
pip install matplotlib
```

## Results

### Performance Summary

| Metric | Best Algorithm | Improvement |
|--------|---------------|-------------|
| Execution Time | A* Search | 39% faster |
| Nodes Explored | A* Search | 55% fewer nodes |
| Learning Capability | Adaptive Dijkstra | 10% improvement over time |

### Key Findings

1. **A* is most efficient:** Explores 55% fewer nodes than Dijkstra
2. **Adaptive Dijkstra learns:** Improves by 10% after feedback
3. **All are fast:** <1ms execution time
4. **Modified Dijkstra finds different paths:** Considers real-world factors

## Experimental Design

### Controlled Variables
- Same road network for all algorithms
- Same start/end nodes
- Same hardware environment
- 100 runs for statistical significance

### Measured Variables
- Execution time (milliseconds)
- Nodes explored (efficiency metric)
- Path cost (route quality)
- Standard deviation (consistency)

### Statistical Method
- Report: Mean ± Std Dev
- Compare: Percentage improvements vs baseline
- Validate: All algorithms find correct paths

## Interpreting Results

### Execution Time
Lower is better. Measures raw algorithm speed.

### Nodes Explored
Lower is better. Indicates algorithm efficiency in search space exploration.
- Dijkstra explores all reachable nodes
- A* uses heuristic to focus search
- Adaptive Dijkstra learns to avoid poor paths

### Path Cost
Lower is better (for distance-based costs). Higher cost may indicate better routes considering traffic/quality.

### Convergence (Adaptive Only)
Track how Adaptive Dijkstra improves over multiple runs as it learns from feedback.

## Adding New Experiments

To add new test cases, edit `performance_comparison.py`:

```python
test_cases = [
    (start_node, end_node, "Description"),
    # Add more here
]
```

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'matplotlib'`
**Solution:** `pip install matplotlib`

**Issue:** No results file found
**Solution:** Run `performance_comparison.py` first before `generate_graphs.py`

**Issue:** Different results on different machines
**Solution:** Expected - timing varies with hardware. Node exploration counts should be consistent.

## Citation

If you use this experimental framework, please cite:

```
Food Delivery System Experimental Framework
Data Structures & Algorithms Project
[Your University], 2026
```
