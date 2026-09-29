import colorsys
import math
import random
import tkinter
import time
import turtle


WINDOW_SIZE = 800
PARTICLE_COUNT = 700
HEART_PARTICLE_COUNT = 200
TRAIL_LENGTH = 8
PARTICLE_RADIUS = 3.0
FRAME_COUNT = 500


def heart_point(angle):
    """Return a point on the parametric heart curve."""
    x = 16 * math.sin(angle) ** 3 * 15
    y = (
        13 * math.cos(angle)
        - 5 * math.cos(2 * angle)
        - 2 * math.cos(3 * angle)
        - math.cos(4 * angle)
    ) * 15
    return x, y


def evenly_spaced_angles(count):
    sample_count = 2000
    samples = [2 * math.pi * index / sample_count for index in range(sample_count + 1)]
    distances = [0.0]

    for index in range(sample_count):
        start = heart_point(samples[index])
        end = heart_point(samples[index + 1])
        distances.append(
            distances[-1] + math.hypot(end[0] - start[0], end[1] - start[1])
        )

    angles = []
    total_length = distances[-1]
    for index in range(count):
        wanted_distance = total_length * index / count
        segment = next(
            segment
            for segment, distance in enumerate(distances[1:], start=1)
            if distance >= wanted_distance
        )
        segment_length = distances[segment] - distances[segment - 1]
        progress = (
            (wanted_distance - distances[segment - 1]) / segment_length
            if segment_length
            else 0.0
        )
        angles.append(
            samples[segment - 1]
            + progress * (samples[segment] - samples[segment - 1])
        )

    return angles


def particle_color(x, y):
    energy = max(0.0, 1 - math.hypot(x, y) / 400)
    red, green, blue = colorsys.hsv_to_rgb((0.7 + energy * 0.3) % 1.0, 0.9, 1.0)
    return "#%02x%02x%02x" % (int(red * 255), int(green * 255), int(blue * 255))


def create_particles(canvas, outline_angles):
    particles = []
    total_count = PARTICLE_COUNT + HEART_PARTICLE_COUNT

    for index in range(total_count):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(50, 300)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        item = canvas.create_oval(
            x - PARTICLE_RADIUS,
            -y - PARTICLE_RADIUS,
            x + PARTICLE_RADIUS,
            -y + PARTICLE_RADIUS,
            fill="#ffffff",
            outline="",
        )
        is_outline = index >= PARTICLE_COUNT
        scale = 1.0 if is_outline else random.uniform(0.2, 1.0)
        offset = (
            outline_angles[index - PARTICLE_COUNT]
            if is_outline
            else random.choice(outline_angles) + random.uniform(0, 0.05)
        )
        particles.append({"x": x, "y": y, "item": item, "scale": scale,
                          "trail": [], "trail_on": is_outline, "offset": offset})

    return particles


def animate(screen, canvas, particles):
    for frame in range(FRAME_COUNT):
        rotation = frame * 0.02
        for particle in particles:
            x, y = particle["x"], particle["y"]
            target = heart_point((rotation + particle["offset"]) % (2 * math.pi))
            next_x = x + (target[0] * particle["scale"] - x) * 0.15
            next_y = y + (target[1] * particle["scale"] - y) * 0.15
            color = particle_color(x, y)
            item = particle["item"]

            canvas.coords(
                item,
                next_x - PARTICLE_RADIUS,
                -next_y - PARTICLE_RADIUS,
                next_x + PARTICLE_RADIUS,
                -next_y + PARTICLE_RADIUS,
            )
            canvas.itemconfig(item, fill=color)

            if particle["trail_on"]:
                trail = particle["trail"]
                trail.append(canvas.create_line(x, -y, next_x, -next_y, fill=color, width=1))
                if len(trail) > TRAIL_LENGTH:
                    canvas.delete(trail.pop(0))

            particle["x"], particle["y"] = next_x, next_y

        screen.update()


def main():
    screen = turtle.Screen()
    screen.setup(width=WINDOW_SIZE, height=WINDOW_SIZE)
    screen.bgcolor("#000000")
    screen.title("Nebula Heart")
    screen.tracer(0)
    screen.delay(0)
    canvas = screen.getcanvas()
    outline_angles = evenly_spaced_angles(HEART_PARTICLE_COUNT)
    particles = create_particles(canvas, outline_angles)

    screen.update()
    time.sleep(1.5)
    try:
        animate(screen, canvas, particles)
    except (tkinter.TclError, turtle.Terminator):
        return
    turtle.done()


if __name__ == "__main__":
    main()