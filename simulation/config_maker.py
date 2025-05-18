import json
from pathlib import Path

class ConfigError(Exception):
    pass

class Config:
    def __init__(self, config_path: str):
        path = Path(config_path)
        
        if not path.is_file():
            raise ConfigError(f"Config file not found at {config_path}")
        
        try:
            with path.open("r") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Failed to parse JSON config at {config_path}.\nError: {e}")
        
        try:
            sim = config["simulation"]
            beh = config["behavior"]
            out = config["output"]

            # Simulation
            self.num_boids = int(sim["boid_count"])
            self.frames = int(sim["frames"])
            self.width = int(sim["space_width"])
            self.height = int(sim["space_height"])

            # Behavior
            self.perception_radius = beh["perception_radius"]
            self.separation_distance = beh["separation_distance"]
            self.max_speed = beh["max_speed"]
            self.max_force = beh["max_force"]
            self.alignment_weight = beh["alignment_weight"]
            self.cohesion_weight = beh["cohesion_weight"]
            self.separation_weight = beh["separation_weight"]

            # Output
            self.output_dir = Path(out["output_dir"]).resolve()

        except KeyError as e:
            raise ConfigError(f"Missing key in config file: {e}")
