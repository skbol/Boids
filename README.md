# Boids Simulation (2D)

Just a simple 2D boids simulation I'm building in Python.

This project implements a **2D Boids simulation engine** written in Python. The simulation models the flocking/herding behavior of boids — simple agents following basic rules like separation, alignment, and cohesion — producing emergent collective motion. 

<img src="assets\boids_simulation.gif" alt="Boids Simulation Interactive Demo" width="500"/>


---

## How It Works

- The simulation runs independently of any graphics library.
- For each frame, it saves the position of every boid to disk.
- You can then use any rendering method (Pygame, WebGL, or even your own tools) to visualize the output.

---

## Key Features

- **Pure simulation logic, decoupled from rendering** `Use run.py`       
  The engine focuses solely on the physics and behavior simulation. It outputs the boids' positions frame-by-frame into files.

- **Optional live render**
    Interactively control the simulation (requires pygame) `Use interactive.py`

- **Modular and extensible design**  
  Clean separation of concerns allows easy integration with various rendering engines.

---

## Current Features

- Boids with basic rules (alignment, separation, cohesion)
- 2D vector math using a small custom class (no numpy dependency)
- Output written as JSON (one file per run)

---

## Upcoming Enhancements

- **QuadTree and other spatial search optimizations**  
  To improve simulation performance by efficiently querying nearby boids.

- **Scripts and tools for multiple rendering engines**  
  Providing ready-to-use code for rendering the output in Blender, WebGL, and Unity etc.

- **Binary format intermediate artifacts**  
  Compact, high-performance binary serialization (e.g., MessagePack or NumPy binary formats) as alternatives to JSON for large-scale simulations.

---

## Usage

1. Run the simulation script `python run.py` to generate output json data or use `python interactive.py` to run the live render.      

2. Use your preferred rendering engine (Pygame, WebGL, Unity, etc.) to load and visualize the output data.

---
