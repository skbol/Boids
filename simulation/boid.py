"""
Author: Srikanth Bolla
"""

import math
import random
from simulation.vector import Vector2D

class Boid:
    def __init__(self, config):
        ''' Each boid will have 3 main parameters
        1. Position vector - Tracks where the location of boid in the field
        2. Velocity vector - Tracks the direction and magnitude(speed) of boid's motion
        3. Acceleration vector - For a boid to steer, we use changes in velocity vector (represented as acceleration)
        '''
        # Configurable parameters
        self.config = config
        
        # Boid parameters
        # Spawn the boid in a random position within the bounds
        self.position = Vector2D(random.uniform(0, self.config.width), random.uniform(0, self.config.height))
        
        # Random angle between 0 and 2.Pi radians (i.e Full circle) for velocity's direction
        angle = random.uniform(0, 2 * math.pi)
        
        # velocity vector with 'max_speed' magnitude
        self.velocity = Vector2D(math.cos(angle), math.sin(angle)) * self.config.max_speed
        
        # Initialize with no acceleration
        self.acceleration = Vector2D.zero()

    def _distance_to(self, boid: "Boid") -> float:
        # Calculate the distance between two boids using vector magnitude
        return (self.position - boid.position).magnitude()

    def _get_neighbors(self, all_boids: list["Boid"]) -> list["Boid"]:
        # Check if the distance between two boids is less than perception radius
        neighbors = [boid for boid in all_boids if boid is not self and self._distance_to(boid) < self.config.perception_radius]
        return neighbors

    def _cohesion(self, neighbors):
        # Compute the cohesion steering force toward the average position of neighbors
        if not neighbors:
            return Vector2D.zero()

        # Calculate average position of neighbors
        avg_pos = Vector2D.zero()
        for boid in neighbors:
            avg_pos += boid.position

        avg_pos = avg_pos / len(neighbors)  # mean position

        # Create a vector pointing from current position to average position (desired velocity)
        desired = avg_pos - self.position
    
        # Normalize desired vector and scale to max speed
        desired = desired.normalize() * self.config.max_speed

        # Steering force = desired velocity - current velocity
        steering = desired - self.velocity
    
        # Limit the magnitude of steering force to max_force
        if steering.magnitude() > self.config.max_force:
            steering = steering.normalize() * self.config.max_force

        return steering

    def _alignment(self, neighbors):
        # Compute the alignment steering force toward the average velocity of neighbors
        if not neighbors:
            return Vector2D.zero()

        # Calculate average velocity of neighbors
        avg_vel = Vector2D.zero()
        for boid in neighbors:
            avg_vel += boid.velocity

        avg_vel = avg_vel / len(neighbors)  # mean velocity

        # Normalize average velocity and scale to max speed (desired velocity)
        desired = avg_vel.normalize() * self.config.max_speed

        # Steering force = desired velocity - current velocity
        steering = desired - self.velocity

        # Limit steering force magnitude to max_force
        if steering.magnitude() > self.config.max_force:
            steering = steering.normalize() * self.config.max_force

        return steering

    def _separation(self, neighbors):
        # Compute the separation steering force away from local neighbors
        steering = Vector2D.zero()
        total = 0

        for boid in neighbors:
            distance = self._distance_to(boid)

            # Only consider neighbors closer than separation_distance
            if distance < self.config.separation_distance and distance > 0:
                # Vector pointing away from neighbor weighted by inverse distance
                diff = self.position - boid.position
                diff = diff.normalize() / distance
                steering += diff
                total += 1

        if total > 0:
            steering = steering / total

        if steering.magnitude() > 0:
            # Normalize and scale to max speed (desired velocity)
            steering = steering.normalize() * self.config.max_speed

            # Steering force = desired velocity - current velocity
            steering = steering - self.velocity

            # Limit to max_force
            if steering.magnitude() > self.config.max_force:
                steering = steering.normalize() * self.config.max_force

        return steering
    
    def _wraparound(self):
        # Wraparound: If the boid goes out of bounds, wrap it back to the other side (toroidal space)
        self.position.x %= self.config.width
        self.position.y %= self.config.height
    
    def _keep_in_bounds(self, margin=100, turn_factor=1):
        # Keeps the boids in the bounds by applying turning forces when close to bounds
        if self.position.x < margin:
            self.acceleration += Vector2D(turn_factor, 0)
        elif self.position.x > self.config.width - margin:
            self.acceleration += Vector2D(-turn_factor, 0)

        if self.position.y < margin:
            self.acceleration += Vector2D(0, turn_factor)
        elif self.position.y > self.config.height - margin:
            self.acceleration += Vector2D(0, -turn_factor)
    
    def compute_steerings(self, all_boids: list["Boid"]) -> None:
        '''Compute the steering forces for the boid'''

        neighbors = self._get_neighbors(all_boids)
        
        cohesion_force = self._cohesion(neighbors) * self.config.cohesion_weight
        alignment_force = self._alignment(neighbors) * self.config.alignment_weight
        separation_force = self._separation(neighbors) * self.config.separation_weight
        
        # Note that since F=ma and we consider each boid as unit mass, we can say F = acceleration
        # Hence, we can say acceleration = Steering forces exerted on a boid 
        # (cohesionSteering + alignmentSterring + separationSteering) 
        self.acceleration += cohesion_force
        self.acceleration += alignment_force
        self.acceleration += separation_force
        
        self._keep_in_bounds()

    def update(self) -> None:
        ''' Apply the position updates using the pre-calculated acceleration vector'''

        # Update velocity by adding acceleration vector
        self.velocity += self.acceleration
        
        # Limit speed to max_speed if velocity magnitude exceeds it
        if self.velocity.magnitude() > self.config.max_speed:
            self.velocity = self.velocity.normalize() * self.config.max_speed

        # Update position by velocity vector
        self.position += self.velocity

        # After updating the position, the boid might go out of bounds
        # Happens if the turn_factor is not strong enough to counteract the steering forces
        # Counteract this by wrapping the boid back into bounds (toroidal space)
        self._wraparound()
        
        # Reset acceleration to zero for the next frame's computations
        self.acceleration = Vector2D.zero()

