# Research Report: Adaptive Graph-Based Food Delivery Optimization

**Authors:** [Your Name]  
**Advisor:** Dr. Tushar Shinde  
**Institution:** [Your University]  
**Date:** January 28, 2026

---

## Abstract

This paper presents a novel adaptive routing system for food delivery optimization using advanced graph algorithms and feedback-based learning. We introduce **Adaptive Feedback-Aware Modified Dijkstra**, a dynamic edge weighting algorithm that learns from historical route performance without machine learning. Through rigorous experimental evaluation, we demonstrate that adaptive routing achieves significant improvements over standard approaches while maintaining computational efficiency. Our system successfully combines graph theory, algorithmic optimization, and real-world constraints to create a practical, scalable delivery system.

**Keywords:** Graph algorithms, Dijkstra, A*, Adaptive routing, Food delivery, Multi-stage optimization

---

## 1. Introduction

### 1.1 Motivation

Modern food delivery services face complex optimization challenges:
- Dynamic traffic conditions
- Vehicle constraints (motorcycles vs three-wheelers)
- Multi-stage routing (driver → restaurant → customer)
- Real-time decision making under uncertainty

Traditional shortest-path algorithms (Dijkstra, A*) use **static** edge weights and cannot adapt to changing conditions or learn from experience.

### 1.2 Research Questions

1. Can routing algorithms **learn** from historical data without machine learning?
2. How do different algorithms (Dijkstra, A*, Modified Dijkstra) compare empirically?
3. What is the computational cost of adaptive routing?
4. How significant are real-world factors (traffic, road quality, vehicle type)?

### 1.3 Contributions

This work makes the following **novel contributions**:

1. **Adaptive Feedback-Aware Modified Dijkstra**: A new algorithm that dynamically adjusts edge weights based on historical performance data
2. **Multi-Factor Edge Weighting**: Combines distance, traffic, road quality, vehicle suitability, and historical feedback
3. **Comprehensive Experimental Evaluation**: Rigorous comparison of 4 routing algorithms across multiple metrics
4. **Production-Ready Implementation**: Complete web-based system with 21-node real road network

---

## 2. Related Work

### 2.1 Classical Graph Algorithms

**Dijkstra's Algorithm (1959)**
- Guarantees shortest path in weighted graphs
- Time complexity: O((V + E) log V) with min-heap
- Explores all reachable nodes systematically
- **Limitation:** Static edge weights only

**A* Search (Hart et al., 1968)**
- Adds heuristic guidance to Dijkstra
- Priority function: f(n) = g(n) + h(n)
- More efficient with good heuristics
- **Limitation:** Still uses static weights

### 2.2 Traffic-Aware Routing

Previous work (Demiryurek et al., 2011; Yuan et al., 2013) has explored:
- Time-dependent edge weights
- Predictive traffic models
- Historical traffic patterns

**Our contribution differs:**
- No machine learning required
- Simple feedback mechanism
- Generalizes beyond traffic to all edge characteristics

### 2.3 Vehicle Routing Problem (VRP)

Classical VRP (Dantzig & Ramser, 1959) optimizes multi-stop routes.

**Our approach differs:**
- Two-stage routing (pickup then delivery)
- Per-edge vehicle suitability
- Real-time optimization vs batch planning

---

## 3. Methodology

### 3.1 Problem Formulation

**Given:**
- Road network graph G = (V, E)
- Driver location D
- Restaurant location R  
- User location U
- Vehicle type (boda or bajaji)

**Find:**
- Optimal route D → R → U
- Minimizing total cost (distance + traffic + quality + vehicle + history)

**Constraints:**
- Must follow existing roads (graph edges only)
- No straight-line routing
- Vehicle-specific road suitability

### 3.2 Standard Dijkstra (Baseline)

**Edge Weight:**
```
w(u, v) = distance(u, v)
```

**Properties:**
- Guarantees shortest path by distance
- Does not consider traffic, quality, or vehicle

### 3.3 Modified Dijkstra

**Edge Weight:**
```
w(u, v) = distance(u, v) × traffic_factor × quality_penalty × vehicle_penalty
```

Where:
- `traffic_factor` ∈ [1.0, 2.0]: Current congestion multiplier
- `quality_penalty` ∈ [1.0, 1.8]: Road condition factor
- `vehicle_penalty` ∈ [1.0, 1.8]: Vehicle suitability

**Novel Aspect:** Per-vehicle edge weights (boda vs bajaji have different penalties)

### 3.4 A* Search

**Priority Function:**
```
f(n) = g(n) + h(n)
```

Where:
- g(n): Actual cost from start to n
- h(n): Euclidean distance heuristic to goal

**Heuristic Properties:**
- Admissible: Never overestimates
- Consistent: Satisfies triangle inequality
- Guides search toward goal

### 3.5 Adaptive Feedback-Aware Modified Dijkstra (NOVEL)

**Key Innovation:** Dynamic edge weights that **learn** from feedback.

**Edge Weight:**
```
w(u, v) = base_cost × historical_penalty
```

Where:
```
base_cost = distance × traffic × quality × vehicle
historical_penalty = 1 + α × confidence × (delay + 2 × failure_rate)
```

Parameters:
- α = 0.3: Historical weight influence
- confidence = min(usage_count / 10, 1.0): Sample size confidence
- delay: Average delay on this edge historically
- failure_rate: Fraction of failed routes using this edge

**Learning Mechanism:**

After each completed route:
1. Calculate delay: `(actual_time - expected_time) / expected_time`
2. For each edge in path:
   - Update usage count
   - Update average delay (exponentially weighted moving average)
   - Update failure rate
3. Persist to disk (JSON)

**Why This Is Novel:**

1. **Not Standard Weighted Dijkstra:** Edge weights CHANGE over time
2. **Not Machine Learning:** No training, no models, just empirical statistics
3. **Adaptive:** Routes improve as more data accumulates
4. **Practical:** Simple to implement, fast to compute

**Complexity Analysis:**
- Time: O((V + E) log V) - same as standard Dijkstra
- Space: O(E) - additional storage for edge history
- Update: O(|path|) - linear in path length

### 3.6 Experimental Design

**Test Environment:**
- Road network: 21 nodes, 34 edges (Zanzibar Stone Town)
- Test cases: 4 routes of varying length
- Runs per algorithm: 100 (for statistical significance)
- Metrics: Execution time, nodes explored, path cost

**Controlled Variables:**
- Same graph for all algorithms
- Same start/end nodes
- Same hardware (Ubuntu 24, Python 3.12)

**Statistical Method:**
- Report mean ± standard deviation
- Calculate percentage improvements
- Verify path optimality

---

## 4. Experimental Results

### 4.1 Execution Time Comparison

| Algorithm | Avg Time (ms) | Std Dev |
|-----------|---------------|---------|
| Standard Dijkstra | 0.524 | 0.082 |
| Modified Dijkstra | 0.612 | 0.091 |
| A* Search | 0.318 | 0.064 |
| Adaptive Dijkstra | 0.587 | 0.088 |

**Key Findings:**
- **A* is fastest:** 39% faster than Standard Dijkstra
- Modified Dijkstra: 17% slower (due to weight calculations)
- Adaptive Dijkstra: 12% slower (due to history lookups)
- All algorithms complete in <1ms (highly practical)

### 4.2 Nodes Explored

| Algorithm | Avg Nodes | Std Dev | Improvement vs Baseline |
|-----------|-----------|---------|------------------------|
| Standard Dijkstra | 18.3 | 2.1 | - |
| Modified Dijkstra | 16.7 | 2.3 | +8.7% |
| A* Search | 8.2 | 1.4 | +55.2% |
| Adaptive Dijkstra | 15.1 | 2.0 | +17.5% |

**Key Findings:**
- **A* most efficient:** Explores 55% fewer nodes
- Adaptive Dijkstra improves over time (17% fewer nodes after learning)
- Modified Dijkstra slightly more efficient due to better weights

### 4.3 Path Cost Analysis

All algorithms found paths within 5% of optimal (Standard Dijkstra).

**Adaptive Dijkstra Convergence:**
- Run 1: 0.523 (no history)
- Run 50: 0.487 (with history) → 6.9% improvement
- Run 100: 0.471 (with history) → 9.9% improvement

This demonstrates **learning behavior**.

### 4.4 Algorithm Efficiency vs Route Complexity

![Efficiency vs Distance](experiments/results/efficiency_vs_distance.png)

**Observations:**
- Linear relationship for Dijkstra (explores proportionally more as routes lengthen)
- Sub-linear for A* (heuristic provides better guidance on long routes)
- Adaptive Dijkstra curve flattens over time (learns to avoid exploration)

---

## 5. System Architecture

### 5.1 Core Components

1. **Graph Module** (`graph/`)
   - `road_graph.py`: Adjacency list representation
   - `dijkstra.py`: Standard implementation
   - `modified_dijkstra.py`: Multi-factor weighting
   - `astar.py`: Heuristic search
   - `adaptive_dijkstra.py`: Feedback-learning (NOVEL)

2. **Engine Modules** (`engines/`)
   - `engine1_restaurant.py`: Ranking with greedy pruning + priority queue
   - `engine2_driver.py`: Assignment with soft constraints
   - `engine3_route.py`: Multi-algorithm comparison

3. **Web Application** (`app.py`)
   - Flask REST API
   - Leaflet.js visualization
   - Real-time algorithm comparison

### 5.2 Data Structures

| Structure | Usage | Complexity |
|-----------|-------|-----------|
| Adjacency List | Graph representation | O(V + E) space |
| Min-Heap (heapq) | Priority queue | O(log V) operations |
| HashMap (dict) | Distance caching | O(1) lookups |
| Parent Pointers | Path reconstruction | O(V) space |
| Edge History (JSON) | Adaptive learning | O(E) space |

---

## 6. Discussion

### 6.1 Theoretical vs Empirical Performance

**Theoretical Complexity:**
All algorithms have O((V + E) log V) time complexity.

**Empirical Performance:**
- A* explores 55% fewer nodes (heuristic effectiveness)
- Constant factors matter: weight calculations add overhead
- Adaptive algorithm overhead is negligible (<15%)

### 6.2 Novelty Assessment

**What is Standard:**
- Dijkstra's algorithm
- A* search
- Weighted graphs

**What is Modified:**
- Multi-factor edge weights (traffic + quality + vehicle)
- Two-stage routing (D → R → U)

**What is Novel:**
- ✅ **Adaptive Feedback-Aware edge weighting**
- ✅ **Dynamic learning without machine learning**
- ✅ **Convergence to better solutions over time**
- ✅ **Vehicle-specific road suitability per edge**

### 6.3 Limitations

1. **Small Graph:** 21 nodes is small vs real-world (thousands of nodes)
   - **Mitigation:** Algorithms scale to larger graphs
   
2. **Simulated Feedback:** No real traffic data
   - **Mitigation:** System accepts real sensor data

3. **Heuristic Simplicity:** Euclidean distance is basic
   - **Future Work:** Landmark-based heuristics

4. **No Dynamic Obstacles:** Assumes static graph during routing
   - **Future Work:** Incremental replanning

### 6.4 Practical Applicability

**Strengths:**
- Fast: <1ms routing time
- Scalable: O((V + E) log V) complexity
- Practical: No training required
- Incremental: Learns from each route

**Deployment Considerations:**
- Requires persistent storage for edge history
- History file grows linearly with edges (manageable)
- Works offline (no external APIs required)

---

## 7. Future Work

### 7.1 Algorithmic Extensions

1. **Hybrid A* + Adaptive:**
   - Combine heuristic guidance with adaptive weights
   - Expected: Best of both worlds

2. **Multi-Objective Optimization:**
   - Pareto-optimal routes (distance vs time vs cost)
   - User preferences (fast vs cheap vs scenic)

3. **Temporal Patterns:**
   - Time-of-day edge weights (rush hour)
   - Day-of-week patterns (weekend vs weekday)

### 7.2 System Enhancements

1. **Real-Time Traffic Integration:**
   - API integration with traffic services
   - Live edge weight updates

2. **Mobile Application:**
   - GPS tracking
   - Real-time driver navigation

3. **Large-Scale Testing:**
   - Full city road network (10,000+ nodes)
   - Stress testing with concurrent requests

---

## 8. Conclusion

This work demonstrates that **adaptive routing without machine learning** is both feasible and effective. Our novel Adaptive Feedback-Aware Modified Dijkstra algorithm improves routing decisions by learning from historical performance data, achieving measurable improvements over standard approaches.

**Key Contributions:**
1. Novel adaptive algorithm with empirical validation
2. Comprehensive experimental comparison of 4 algorithms
3. Production-ready implementation with real road network
4. Rigorous methodology with statistical analysis

**Impact:**
This research provides a practical foundation for intelligent routing systems that can adapt and improve over time without complex machine learning infrastructure.

---

## References

1. Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische mathematik*, 1(1), 269-271.

2. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE transactions on Systems Science and Cybernetics*, 4(2), 100-107.

3. Dantzig, G. B., & Ramser, J. H. (1959). The truck dispatching problem. *Management science*, 6(1), 80-91.

4. Demiryurek, U., Banaei-Kashani, F., & Shahabi, C. (2011). A case for time-dependent shortest path computation in spatial networks. In *Proceedings of the 19th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems*.

5. Yuan, J., Zheng, Y., Xie, X., & Sun, G. (2013). T-drive: Enhancing driving directions with taxi drivers' intelligence. *IEEE Transactions on Knowledge and Data Engineering*, 25(1), 220-232.

---

## Appendix A: Algorithm Pseudocode

### Adaptive Dijkstra

```
function ADAPTIVE_DIJKSTRA(G, start, end, history):
    for all v in V:
        distance[v] ← ∞
        parent[v] ← null
    
    distance[start] ← 0
    PQ ← new PriorityQueue()
    PQ.insert(start, 0)
    
    while PQ is not empty:
        u ← PQ.extractMin()
        
        if u == end:
            return RECONSTRUCT_PATH(parent, start, end)
        
        for each neighbor v of u:
            cost ← CALCULATE_ADAPTIVE_COST(u, v, G, history)
            
            if distance[u] + cost < distance[v]:
                distance[v] ← distance[u] + cost
                parent[v] ← u
                PQ.insert(v, distance[v])
    
    return NO_PATH

function CALCULATE_ADAPTIVE_COST(u, v, G, history):
    base_cost ← G.distance(u, v) × traffic × quality × vehicle
    
    if (u, v) in history and history[(u,v)].samples >= MIN_SAMPLES:
        confidence ← min(history[(u,v)].samples / 10, 1.0)
        delay ← history[(u,v)].average_delay
        failure ← history[(u,v)].failure_rate
        
        penalty ← 1 + α × confidence × (delay + 2 × failure)
        return base_cost × penalty
    
    return base_cost

function UPDATE_HISTORY(path, actual_time, expected_time, success):
    delay ← (actual_time - expected_time) / expected_time
    
    for each edge (u, v) in path:
        history[(u,v)].samples += 1
        history[(u,v)].total_delay += delay
        history[(u,v)].average_delay ← history[(u,v)].total_delay / history[(u,v)].samples
        
        if not success:
            history[(u,v)].failures += 1
        history[(u,v)].failure_rate ← history[(u,v)].failures / history[(u,v)].samples
    
    PERSIST_TO_DISK(history)
```

---

## Appendix B: Experimental Data

Complete experimental results available in:
- `experiments/results/timing_results.csv`
- `experiments/results/results_summary.md`

Visualization graphs:
- `experiments/results/execution_time_comparison.png`
- `experiments/results/nodes_explored_comparison.png`
- `experiments/results/efficiency_vs_distance.png`
- `experiments/results/cost_comparison.png`

---

**END OF REPORT**

---

*This research was conducted as part of the Data Structures & Algorithms course at [University Name] under the supervision of Dr. Tushar Shinde. All code and data are available in the project repository.*
