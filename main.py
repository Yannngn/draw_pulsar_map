import json
import math
from turtle import RawTurtle

from cairosvg import svg2png
from PIL import Image
from svg_turtle import SvgTurtle

# TODO: center result in image (earth should be out of center)
# TODO: increase detail of drawing
# TODO: document

W = 1440
H = 1024
SCALE = 1


def get_angle(angle: float):
    if angle < 0:
        return 360 + angle

    return angle


def draw_vertical_line(t: RawTurtle):
    t.penup()
    t.right(90)
    t.forward(SCALE * 0.25)
    t.right(180)

    t.pensize(1)
    t.pendown()
    t.forward(SCALE * 0.5)

    t.penup()
    t.right(180)
    t.forward(SCALE * 0.25)
    t.left(90)


def draw_binary(t: RawTurtle, angle: float, period: str):
    t.penup()
    t.setheading(angle)
    t.forward(SCALE * 0.5)

    for integer in period:
        if int(integer):
            draw_vertical_line(t)
            t.forward(SCALE * 0.25)

            continue

        t.pensize(1)
        t.pendown()
        t.forward(SCALE * 0.25)

        t.penup()
        t.forward(SCALE * 0.25)


def draw_main_line(t: RawTurtle, distance: float, angle: float):
    t.pensize(1)
    t.pendown()
    t.setheading(angle)
    t.forward(distance)

    draw_vertical_line(t)

    t.pensize(1)
    t.pendown()
    t.forward(SCALE * 0.5)


def draw_star(t: RawTurtle, star: dict):
    a = get_angle(star["angle"])
    d = star["distance"] * SCALE

    draw_main_line(t, d, a)
    draw_binary(t, a, star["period"])


def convert_to_rgba(image: Image.Image):
    new_data = []

    image = image.convert("RGBA")
    for item in image.getdata():
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
            continue

        new_data.append(item)

    image.putdata(new_data)

    return image


def config(pulsars):
    global SCALE

    neg_x = pos_x = neg_y = pos_y = max_x = 0

    for pulsar in pulsars:
        d = pulsar["distance"]
        a = pulsar["angle"]
        s = pulsar["period"]

        added_length = sum([0.25 if int(v) else 1.5 for v in s]) + 0.5

        max_x = max(1.5 * (d + added_length), max_x)

        x = (d + added_length) * math.cos(a)
        neg_x = min(x, neg_x)
        pos_x = max(x, pos_x)

        y = (d + added_length) * math.sin(a)
        neg_y = min(y, neg_y)
        pos_y = max(y, pos_y)

    SCALE = min(W / (max_x - neg_x), H / (pos_y - neg_y))

    start_x = -(max_x + neg_x) * SCALE / 2  # (abs(neg_x) - max_x) * SCALE
    start_y = -(pos_y + neg_y) * SCALE / 2

    return start_x, start_y, max_x


def main():
    with open("data/original_pulsars.json", "r") as f:
        pulsars = json.load(f)

    start_x, start_y, max_x = config(pulsars)

    t = SvgTurtle(W, H)
    t.hideturtle()
    t.speed(0)
    t.teleport(start_x, start_y)

    t.pensize(1)
    t.forward(max_x * SCALE)
    t.right(90)
    t.forward(0.5 * SCALE)
    t.right(180)
    t.forward(SCALE)

    for pulsar in pulsars:
        t.teleport(start_x, start_y)

        draw_star(t, pulsar)

    t.save_as("pulsar.svg")

    svg2png(url="pulsar.svg", write_to="pulsar_transparent.png", dpi=300)
    svg2png(
        url="pulsar.svg",
        write_to="pulsar.png",
        dpi=300,
        background_color="white",
    )

    # img = Image.open("pulsar.ps")
    # img.save("pulsar.png", "PNG")
    # img = convert_to_rgba(img)
    # img.save("pulsar_transparent.png", "PNG")


if __name__ == "__main__":
    main()
