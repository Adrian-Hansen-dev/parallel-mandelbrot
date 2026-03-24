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
**Optional: Run the program with dynamic height and width**
```bash
./mandelbrot [height] [width]
```


Check your project folder—you should see a newly generated `mandelbrot_parallel.png` file!
