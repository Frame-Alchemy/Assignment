"""
Lab Work 1: Benchmarking Algorithmic Growth Rates

Objective:
    Empirically investigate constant O(1), logarithmic O(log n),
    linear O(n), n log n O(n log n), quadratic O(n^2), and
    exponential O(2^n) growth patterns.

Submitted by : Sharma Jash Anandkumar, 25BSM058
"""

import time
import random
import sys
import os

# Use non-interactive backend for matplotlib if headless
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# 1. REPRESENTATIVE ALGORITHM IMPLEMENTATIONS

def constant_indexing(arr, index):
    # O(1) - List indexing: accesses an element by index.
    return arr[index]


def logarithmic_binary_search(arr, target):
    # O(log n) - Binary search on a sorted list.
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def linear_search(arr, target):
    # O(n) - Linear search through an unsorted list.
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def merge_sort(arr):
    # O(n log n) - Merge sort.
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    # Merge helper for merge sort.
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quadratic_pair_counter(arr):
    # O(n^2) - Double-loop pair counter (counts pairs where arr[i] == arr[j]).
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                count += 1
    return count


def exponential_subsets(arr):
    # O(2^n) - Exponential subset enumeration (powerset). Safe for small n only!
    result = [[]]
    for elem in arr:
        result += [curr + [elem] for curr in result]
    return result


# 2. BENCHMARKING HARNESS

def time_function(func, *args, trials=5):
    """
    Measures execution time of func(*args) over multiple trials.
    Returns the median elapsed time in seconds.
    Data generation is kept outside this timed block.
    """
    times = []
    for _ in range(trials):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)
    times.sort()
    # Return median
    mid = len(times) // 2
    return times[mid]


def run_benchmarks():
    print("LAB WORK 1: BENCHMARKING ALGORITHMIC GROWTH RATES")
    print()

    results = {}

    # 1. Constant O(1): List Indexing
    print("1. Benchmarking O(1) - List Indexing")
    sizes_const = [1000, 10000, 50000, 100000, 500000, 1000000]
    times_const = []
    for n in sizes_const:
        arr = list(range(n))
        idx = n // 2
        t = time_function(constant_indexing, arr, idx, trials=10)
        times_const.append(t)
    results['O(1) Indexing'] = (sizes_const, times_const)

    # 2. Logarithmic O(log n): Binary Search
    print("2. Benchmarking O(log n) - Binary Search")
    sizes_log = [1000, 10000, 50000, 100000, 500000, 1000000]
    times_log = []
    for n in sizes_log:
        arr = list(range(n))  # Already sorted
        target = -1           # Worst case: not found
        t = time_function(logarithmic_binary_search, arr, target, trials=10)
        times_log.append(t)
    results['O(log n) Binary Search'] = (sizes_log, times_log)

    # 3. Linear O(n): Linear Search
    print("3. Benchmarking O(n) - Linear Search")
    sizes_linear = [1000, 5000, 10000, 25000, 50000, 100000]
    times_linear = []
    for n in sizes_linear:
        arr = list(range(n))
        target = -1  # Worst case: element not present
        t = time_function(linear_search, arr, target, trials=5)
        times_linear.append(t)
    results['O(n) Linear Search'] = (sizes_linear, times_linear)

    # 4. O(n log n): Merge Sort
    print("4. Benchmarking O(n log n) - Merge Sort")
    sizes_nlogn = [500, 1000, 2500, 5000, 10000, 20000]
    times_nlogn = []
    for n in sizes_nlogn:
        arr = [random.randint(0, 100000) for _ in range(n)]
        t = time_function(merge_sort, arr, trials=3)
        times_nlogn.append(t)
    results['O(n log n) Merge Sort'] = (sizes_nlogn, times_nlogn)

    # 5. Quadratic O(n^2): Double-loop Pair Counter
    print("5. Benchmarking O(n^2) - Pair Counter")
    sizes_quad = [200, 400, 800, 1200, 1600, 2000]
    times_quad = []
    for n in sizes_quad:
        arr = [random.randint(0, 50) for _ in range(n)]
        t = time_function(quadratic_pair_counter, arr, trials=3)
        times_quad.append(t)
    results['O(n^2) Pair Counter'] = (sizes_quad, times_quad)

    # 6. Exponential O(2^n): Subset Enumeration (small n only!)
    print("6. Benchmarking O(2^n) - Exponential Subset Enumeration")
    sizes_exp = [10, 12, 14, 16, 18, 20]
    times_exp = []
    for n in sizes_exp:
        arr = list(range(n))
        t = time_function(exponential_subsets, arr, trials=3)
        times_exp.append(t)
    results['O(2^n) Subsets'] = (sizes_exp, times_exp)

    # 3. PRINT COMPARISON TABLES
    print()
    print(f"{'Algorithm':<26} {'Input Sizes (n)':<22} {'Times (seconds)'}")

    for name, (sizes, times) in results.items():
        bound = name.split()[0]
        size_str = f"[{sizes[0]} ... {sizes[-1]}]"
        time_str = f"[{times[0]:.2e}s ... {times[-1]:.2e}s]"
        print(f"{name:<26} {size_str:<22} {time_str}")

    print()

    # Detailed table of results
    print("DETAILED TIMING RESULTS:")
    for name, (sizes, times) in results.items():
        print(f"\n>> {name}:")
        print(f"   {'n':<12} {'Time (seconds)':<18} {'Trend / Growth'}")
        for i, (n, t) in enumerate(zip(sizes, times)):
            ratio_str = ""
            if i > 0 and times[i-1] > 0:
                growth_factor = t / times[i-1]
                ratio_str = f"(x{growth_factor:.2f} from previous)"
            print(f"   {n:<12} {t:<18.6f} {ratio_str}")

    # 4. PLOT EXECUTION TIME AGAINST n
    
    print("\nGenerating benchmark plots")
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle("Empirical Verification of Algorithmic Growth Rates", fontsize=14, fontweight='bold')

    plots_info = [
        ('O(1) Indexing', axes[0, 0], 'blue', 'O(1) - Constant'),
        ('O(log n) Binary Search', axes[0, 1], 'green', 'O(log n) - Logarithmic'),
        ('O(n) Linear Search', axes[0, 2], 'orange', 'O(n) - Linear'),
        ('O(n log n) Merge Sort', axes[1, 0], 'purple', 'O(n log n)'),
        ('O(n^2) Pair Counter', axes[1, 1], 'red', 'O(n^2) - Quadratic'),
        ('O(2^n) Subsets', axes[1, 2], 'brown', 'O(2^n) - Exponential')
    ]

    for key, ax, color, title in plots_info:
        sizes, times = results[key]
        ax.plot(sizes, times, marker='o', color=color, linewidth=2, label='Measured Time')
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('Input Size (n)', fontsize=9)
        ax.set_ylabel('Time (seconds)', fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=8)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_img = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_growth_rates.png")
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"Plot saved successfully to: {out_img}")

    # 5. EXPERIMENTAL LIMITATIONS AND ANALYSIS DISCUSSION

    print("\n")
    print("ANALYSIS AND EXPERIMENTAL OBSERVATIONS:\n")
    print("""
1. O(1) Constant Time:
   - Measured time remains essentially flat across all input sizes (10^3 to 10^6).
   - Small variations are due to CPU cache line hits and background OS noise.

2. O(log n) Logarithmic Time:
   - Binary search execution time grows very slowly; doubling n adds only a single
     comparison (one loop iteration).

3. O(n) Linear Time:
   - Linear search scales proportionally with n; doubling n approximately doubles
     the execution time.

4. O(n log n) Merge Sort:
   - Time scales slightly faster than linear due to the log n tree depth.

5. O(n^2) Quadratic Time:
   - When n increases by a factor of 2, execution time increases roughly by 2^2 = 4x.
   - For n=2000, time is noticeably higher (~0.1s to 0.5s).

6. O(2^n) Exponential Time:
   - Incrementing n by 1 doubles the number of operations and memory required.
   - Tested only up to n=20 (producing 2^20 = 1,048,576 subsets) to avoid OOM
     and CPU starvation.

Experimental Limitations Identified:
- Python interpreter overhead and dynamic type checking create constant-factor delays.
- System scheduling, garbage collection, and CPU thermal throttling introduce timing jitter.
- Timer resolution (perf_counter provides sub-microsecond precision, but cache warming affects initial runs).
""")


if __name__ == "__main__":
    run_benchmarks()
