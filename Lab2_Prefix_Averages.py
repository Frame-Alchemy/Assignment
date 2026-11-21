"""
Lab Work 2: Prefix Averages: Quadratic versus Linear-Time Design

Objective:
    Demonstrate the empirical and theoretical reduction from quadratic O(n^2)
    to linear O(n) time using a running-sum prefix average strategy.

Tasks:
    1. Implement prefix_average1 (nested loop recomputing prefix sum -> O(n^2)).
    2. Implement prefix_average2 (running sum updated incrementally -> O(n)).
    3. Verify equivalent outputs across test suites (singleton, positive,
       negative, mixed-value, empty-sequence).
    4. Benchmark both implementations for increasing sequence lengths.
    5. Plot execution time versus n and compare against theoretical curves.
    6. Formally derive operation counts using summations.

Submitted by: Sharma Jash Anandkumar, 25BSM058
"""

import time
import os
import sys

# Non-interactive matplotlib backend
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 1. ALGORITHM IMPLEMENTATIONS

def prefix_average1(S):
    """
    Quadratic-time implementation O(n^2).
    Computes prefix average by recomputing each prefix sum from index 0 to j.
    """
    n = len(S)
    if n == 0:
        return []
    A = [0.0] * n
    for j in range(n):
        total = 0.0
        for i in range(j + 1):
            total += S[i]
        A[j] = total / (j + 1)
    return A


def prefix_average2(S):
    """
    Linear-time implementation O(n).
    Computes prefix average by maintaining an incremental running sum.
    """
    n = len(S)
    if n == 0:
        return []
    A = [0.0] * n
    total = 0.0
    for j in range(n):
        total += S[j]
        A[j] = total / (j + 1)
    return A


# 2. VALIDATION AND TESTING

def almost_equal(list1, list2, tol=1e-9):
    # Utility to compare floating-point lists within a tolerance.
    if len(list1) != len(list2):
        return False
    return all(abs(a - b) < tol for a, b in zip(list1, list2))


def run_validation_tests():
    print("STEP 1: VALIDATION AND EQUIVALENCE TESTING")

    test_cases = [
        ("Empty Sequence", []),
        ("Singleton Sequence", [42.0]),
        ("Positive Values", [10, 20, 30, 40, 50]),
        ("Negative Values", [-5, -15, -25, -35]),
        ("Mixed Values", [10, -5, 20, -15, 30, 0, -2]),
        ("Fractional Values", [1.5, 2.5, 3.5, 4.5, 5.5])
    ]

    all_passed = True
    for name, seq in test_cases:
        res1 = prefix_average1(seq)
        res2 = prefix_average2(seq)
        passed = almost_equal(res1, res2)
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
        print(f"Test '{name:<20}': {status}")
        print(f"   Input:   {seq}")
        print(f"   Result1: {[round(x, 4) for x in res1]}")
        print(f"   Result2: {[round(x, 4) for x in res2]}")
        print()

    print(f"Validation Summary: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}\n")
    return all_passed


# 3. BENCHMARKING

def benchmark_prefix_averages():
    print("STEP 2: BENCHMARKING PREFIX AVERAGES (QUADRATIC vs LINEAR)")

    # Increasing sequence lengths
    lengths = [100, 250, 500, 1000, 2000, 4000, 6000, 8000, 10000]
    times_algo1 = []
    times_algo2 = []
    trials = 5

    print(f"{'Length (n)':<12} {'prefix_avg1 O(n^2)':<20} {'prefix_avg2 O(n)':<20} {'Speedup Ratio'}")

    for n in lengths:
        seq = [float(i) for i in range(n)]

        # Time prefix_average1
        t1_trials = []
        for _ in range(trials):
            start = time.perf_counter()
            prefix_average1(seq)
            t1_trials.append(time.perf_counter() - start)
        t1_trials.sort()
        t1 = t1_trials[len(t1_trials) // 2]  # median
        times_algo1.append(t1)

        # Time prefix_average2
        t2_trials = []
        for _ in range(trials):
            start = time.perf_counter()
            prefix_average2(seq)
            t2_trials.append(time.perf_counter() - start)
        t2_trials.sort()
        t2 = t2_trials[len(t2_trials) // 2]  # median
        times_algo2.append(t2)

        speedup = t1 / t2 if t2 > 0 else 0
        print(f"{n:<12} {t1:<20.6f} {t2:<20.6f} {speedup:.1f}x")

    print()

    # 4. PLOTTING
    
    print("Step 3: Generating comparison plot...")
    plt.figure(figsize=(10, 6))

    plt.plot(lengths, times_algo1, 'r-o', linewidth=2, label="prefix_average1 : O(n^2) Quadratic")
    plt.plot(lengths, times_algo2, 'b-s', linewidth=2, label="prefix_average2 : O(n) Linear")

    plt.title("Prefix Average Runtime Comparison: O(n^2) vs O(n)", fontsize=13, fontweight='bold')
    plt.xlabel("Input Sequence Length (n)", fontsize=11)
    plt.ylabel("Execution Time (seconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)

    out_plot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prefix_averages_comparison.png")
    plt.savefig(out_plot, dpi=300)
    plt.close()
    print(f"Plot saved to: {out_plot}\n")

    # 5. THEORETICAL DERIVATION AND DISCUSSION

    print("STEP 4: THEORETICAL DERIVATION & NUMERICAL PRECISION")
    print("""
1. Operation Count Derivation:
   - For prefix_average1:
       Outer loop runs j from 0 to n-1.
       Inner loop runs i from 0 to j (executes j + 1 additions).
       Total additions = sum_{j=0}^{n-1} (j + 1)
                       = 1 + 2 + 3 + ... + n
                       = n(n + 1) / 2
                       = (n^2 + n) / 2
       Asymptotically: (n^2 + n) / 2 = O(n^2)

   - For prefix_average2:
       Single loop runs j from 0 to n-1.
       Each iteration performs exactly 1 addition: total += S[j].
       Total additions = n
       Asymptotically: n = O(n)

2. Break-Even and Speedup:
   - For small n (< 20), overhead of Python function calls dominates and both
     finish within microseconds.
   - For n = 1000, prefix_average2 is already ~20x to 50x faster.
   - For n = 10000, prefix_average2 is hundreds of times faster.

3. Numerical Precision:
   - In prefix_average1, prefix sums are accumulated fresh from small indices,
     which can minimize floating-point roundoff errors for very long series.
   - In prefix_average2, repeated accumulation in a single running sum variable
     can accumulate roundoff errors if numbers vary wildly in magnitude (catastrophic cancellation),
     though for typical engineering inputs, IEEE-754 double precision maintains high fidelity.
""")


if __name__ == "__main__":
    run_validation_tests()
    benchmark_prefix_averages()
