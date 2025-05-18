"""
Author: Srikanth Bolla
Description: Run this python file to simulate boid without rendering (headless).
"""

import json
import time
import os
from simulation.config_maker import Config, ConfigError
from simulation.boid import Boid

def run_headless_simulation():
    try:
        config = Config("config.json")
    except ConfigError as e:
        print(f"Config could not be loaded: {e}")
        return

    boids = [Boid(config) for _ in range(config.num_boids)]
    frame_count = config.frames
    output_dir = config.output_dir
    os.makedirs(output_dir, exist_ok=True)

    all_frames = []
    for frame_num in range(frame_count):
        frame_data = {}

        for boid in boids:
            boid.compute_steerings(boids)
        for idx, boid in enumerate(boids):
            boid.update()
            frame_data[f"boid_{idx}"] = {
                "x": boid.position.x,
                "y": boid.position.y
            }

        all_frames.append(frame_data)

    timestamp = int(time.time())
    filename = f"out_frames{frame_count}_time{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        for frame in all_frames:
            json.dump(frame, f)
            f.write("\n")

    print(f"Simulation complete. Output written to {filepath}")

if __name__ == "__main__":
    run_headless_simulation()

