"""
Author: Srikanth Bolla
Description: Run this python file to simulate boid for a interactive visualization (uses pygame).
"""

from simulation.config_maker import Config, ConfigError
import pygame
import sys
import math
import os
import imageio
import shutil
from simulation.boid import Boid

# Constants
FPS = 30
GIF_CAPTURE = False
GIF_DURATION_SEC = 30
CAPTURE_FRAME_LIMIT = GIF_DURATION_SEC * FPS
CAPTURE_DIR = "gif_frames"
GIF_OUTPUT_PATH = "boids_simulation.gif"

def velocity_to_color(velocity, max_speed):
    speed = velocity.magnitude()
    t = max(0.0, min(1.0, speed / max_speed))
    r = int(255 * t)
    g = int(255 * (1 - abs(t - 0.5) * 2))
    b = int(255 * (1 - t))
    return (r, g, b)

def draw_boid(screen, boid, color):
    pos = boid.position
    vel = boid.velocity
    angle = math.atan2(vel.y, vel.x)

    plane_shape = [
        (12, 0), (-8, -6), (-4, -2), (-4, 2), (-8, 6)
    ]

    rotated_points = []
    for x, y in plane_shape:
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        rotated_points.append((pos.x + rotated_x, pos.y + rotated_y))

    pygame.draw.polygon(screen, color, rotated_points)

class InputField:
    def __init__(self, x, y, w, h, label, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = str(text)
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.label = label
        self.label_surface = self.font.render(label, True, (0, 0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isdigit() or event.unicode == '.':
                    self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.label_surface, (self.rect.x, self.rect.y - 20))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return 0.0

def make_gif():
    images = []
    filenames = sorted(os.listdir(CAPTURE_DIR))
    for filename in filenames:
        if filename.endswith(".png"):
            path = os.path.join(CAPTURE_DIR, filename)
            images.append(imageio.imread(path))
    imageio.mimsave(GIF_OUTPUT_PATH, images, fps=FPS)
    print(f"✅ GIF saved as: {GIF_OUTPUT_PATH}")
    shutil.rmtree(CAPTURE_DIR)

def run_simulation():
    try:
        config = Config("config.json")
    except ConfigError as e:
        print(f"Config could not be loaded: {e}")
        return

    pygame.init()
    FONT = pygame.font.SysFont(None, 24)
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("Simulating Boid's Algorithm")
    clock = pygame.time.Clock()

    input_fields = [
        InputField(10, 40, 160, 30, "Cohesion Weight", config.cohesion_weight, FONT),
        InputField(10, 100, 160, 30, "Separation Weight", config.separation_weight, FONT),
        InputField(10, 160, 160, 30, "Alignment Weight", config.alignment_weight, FONT),
        InputField(10, 220, 160, 30, "Number of Boids", config.num_boids, FONT),
        InputField(10, 280, 160, 30, "Perception Radius", config.perception_radius, FONT),
    ]

    boids = [Boid(config) for _ in range(config.num_boids)]

    # GIF setup
    frame_count = 0
    if GIF_CAPTURE:
        os.makedirs(CAPTURE_DIR, exist_ok=True)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((227, 227, 227))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for field in input_fields:
                field.handle_event(event)

        config.cohesion_weight = input_fields[0].get_value()
        config.separation_weight = input_fields[1].get_value()
        config.alignment_weight = input_fields[2].get_value()
        new_num_boids = int(input_fields[3].get_value())
        config.perception_radius = input_fields[4].get_value()

        if new_num_boids != len(boids) and new_num_boids > 0:
            boids = [Boid(config) for _ in range(new_num_boids)]

        for boid in boids:
            boid.compute_steerings(boids)

        for boid in boids:
            boid.update()
            color = velocity_to_color(boid.velocity, config.max_speed)
            draw_boid(screen, boid, color)

        for field in input_fields:
            field.draw(screen)

        pygame.display.flip()

        # Save current frame
        if GIF_CAPTURE and frame_count < CAPTURE_FRAME_LIMIT:
            path = os.path.join(CAPTURE_DIR, f"frame_{frame_count:04d}.png")
            pygame.image.save(screen, path)
            frame_count += 1
        elif GIF_CAPTURE and frame_count == CAPTURE_FRAME_LIMIT:
            make_gif()
            frame_count += 1  # prevent re-saving

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_simulation()
