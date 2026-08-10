import os
import time

import matplotlib.pyplot as plt
import numpy as np


def benchmark():
    sizes = [10**3, 10**4, 10**5, 10**6, 10**7]
    iterative_times = []
    vectorized_times = []

    for size in sizes:
        # Generate dummy price data
        prices = np.random.lognormal(mean=0.001, sigma=0.02, size=size)
        prices[0] = 100.0
        prices = np.cumprod(prices)
        
        # 1. Iterative Approach
        start_time = time.perf_counter()
        returns_iter = np.zeros(size - 1)
        for i in range(1, size):
            returns_iter[i-1] = (prices[i] - prices[i-1]) / prices[i-1]
        iterative_time = time.perf_counter() - start_time
        iterative_times.append(iterative_time)

        # 2. Vectorized Approach (NumPy)
        start_time = time.perf_counter()
        # Equivalent to pct_change
        _ = (prices[1:] - prices[:-1]) / prices[:-1]
        vectorized_time = time.perf_counter() - start_time
        vectorized_times.append(vectorized_time)

        print(f"N={size:,}: Iterative={iterative_time:.6f}s, Vectorized={vectorized_time:.6f}s, Speedup={iterative_time/vectorized_time:.1f}x")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, iterative_times, marker='o', label='Iterative (for loop)', linewidth=2, color='#e74c3c')
    plt.plot(sizes, vectorized_times, marker='s', label='Vectorized (NumPy)', linewidth=2, color='#2ecc71')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Dataset Size (N observations)', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Performance Comparison: Iterative vs Vectorized Operations', fontsize=14, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # Save to architecture folder
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'architecture')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'vectorization_benchmark.pdf')
    plt.savefig(out_path, format='pdf', dpi=300)
    print(f"Saved plot to {out_path}")

if __name__ == "__main__":
    benchmark()
