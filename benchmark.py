import subprocess
import re
import matplotlib.pyplot as plt

# Thread counts we want to test (1 = serial baseline, then doubling up)
thread_counts = [1, 2, 4, 8]
times = []

# Run the mandelbrot program once for each thread count
for t in thread_counts:
    print(f"Running with {t} threads...")

    # subprocess.run starts the mandelbrot program as if we typed it in the terminal
    # capture_output=True grabs the printed text so we can read the time from it
    result = subprocess.run(
        ["./mandelbrot", "2048", "2048", "1000", str(t)],
        capture_output=True, text=True
    )

    # The program prints something like "RECHENZEIT: 3.7335 Sekunden"
    # We use regex to find and extract just the number
    output = result.stdout
    match = re.search(r"RECHENZEIT:\s+([\d.]+)", output)
    time = float(match.group(1))
    times.append(time)
    print(f"  {t} threads: {time:.4f}s")

# Calculate speedup: T_s / T_n
# T_s = serial time (1 thread), T_n = time with n threads
# Example: if 1 thread takes 4s and 4 threads take 1s, speedup = 4/1 = 4x
serial_time = times[0]
speedups = [serial_time / t for t in times]

# Print a nice summary table
print("\n--- Results ---")
for i in range(len(thread_counts)):
    print(f"Threads: {thread_counts[i]}, Time: {times[i]:.4f}s, Speedup: {speedups[i]:.2f}x")

# Create the speedup graph
plt.figure(figsize=(8, 5))

# Blue line = our actual measured speedup
plt.plot(thread_counts, speedups, 'bo-', label='Measured Speedup')

# Red dashed line = ideal/perfect speedup (if 4 threads = exactly 4x faster)
# In reality we never reach this because of overhead
plt.plot(thread_counts, thread_counts, 'r--', label='Ideal (linear) Speedup')

plt.xlabel('Number of Threads')
plt.ylabel('Speedup (T_s / T_n)')
plt.title('Mandelbrot Parallel Speedup')
plt.legend()
plt.xticks(thread_counts)
plt.grid(True)

# Save the graph as an image for the report
plt.savefig('speedup_graph.png', dpi=150)
plt.show()
print("Graph saved as speedup_graph.png")
