# OpenMP Image Processor

This is a C project that uses OpenMP for parallel multi-threading and the `stb` library for image handling. 

To ensure this project builds perfectly on any operating system (macOS, Windows, or Linux) without complex compiler configurations, it runs inside a standardized **VS Code Dev Container**.

## Prerequisites

Before starting, ensure you have the following installed:
1. **Docker Desktop** (Make sure the app is open and running)
2. **Visual Studio Code**
3. The **Dev Containers** extension for VS Code

## How to Start the Environment

1. Clone this repository and open the project folder in VS Code.
2. A prompt might appear in the bottom right asking if you want to reopen the folder in a container. If so, click **Reopen in Container**.
3. If no prompt appears, open the Command Palette (`Cmd + Shift + P` on Mac, `Ctrl + Shift + P` on Windows/Linux).
4. Type and select: **Dev Containers: Reopen in Container**.

*Note: The first time you do this, it will take a minute or two to build the Linux environment.*

## How to Build and Run

Once the container is running, open a new terminal inside VS Code (`Ctrl + ~` or **Terminal > New Terminal**). Because you are now inside a Linux container, you can use standard GCC commands.

**1. Compile the code:**
```bash
gcc src/main.c -o mandelbrot -fopenmp -O3 -lm
```

**2. Run the program:**
```bash
./mandelbrot
```

**Optional: Custom width and height**
```bash
./mandelbrot 1024 1024
```

**Optional: Custom width, height and max iterations**
```bash
./mandelbrot 1024 1024 500
```

**Optional: Set thread count (for benchmarking)**
```bash
./mandelbrot 1024 1024 500 4
```

**Optional: Full control with viewport (min_x, min_y, max_x, max_y)**
```bash
./mandelbrot 1024 1024 500 -2.0 -1.0 1.0 1.0
```

**Optional: Full control with viewport and thread count**
```bash
./mandelbrot 1024 1024 500 -2.0 -1.0 1.0 1.0 4
```

Check your project folder—you should see a newly generated `mandelbrot_parallel.png` file!

## Benchmarking

To run the benchmark and generate a speedup graph:

```bash
python3 benchmark.py
```

This runs the Mandelbrot computation with 1, 2, 4, and 8 threads, measures the time, and saves a speedup graph as `speedup_graph.png`.
