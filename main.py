import json
import turtle
from turtle import Turtle

from PIL import Image

WORLD_SCALE = 24
CUT = WORLD_SCALE * 0.5


# TODO: center result in image (earth should be out of center)
# TODO: increase detail of drawing
# TODO: document


def get_angle(angle: float):
    if angle < 0:
        return 360 + angle

    return angle


def draw_vertical_line(turtle: Turtle):
    turtle.penup()
    turtle.right(90)
    turtle.forward(CUT * 0.5)
    turtle.right(180)

    turtle.pendown()
    turtle.forward(CUT)

    turtle.penup()
    turtle.right(180)
    turtle.forward(CUT * 0.5)
    turtle.left(90)


def draw_binary(turtle: Turtle, angle: float, period: str):
    turtle.penup()
    turtle.setheading(angle)
    turtle.forward(CUT)

    for integer in period:
        if int(integer):
            draw_vertical_line(turtle)
            turtle.forward(CUT * 0.5)

            continue

        turtle.pendown()
        turtle.forward(CUT * 0.5)

        turtle.penup()
        turtle.forward(CUT * 0.5)


def draw_main_line(turtle: Turtle, distance: float, angle: float):
    turtle.pendown()
    turtle.setheading(angle)
    turtle.forward(distance)

    draw_vertical_line(turtle)

    turtle.pendown()
    turtle.forward(CUT)


def draw_star(turtle: Turtle, star: dict):
    a = get_angle(star["angle"])
    d = star["distance"] * WORLD_SCALE

    draw_main_line(turtle, d, a)
    draw_binary(turtle, a, star["period"])


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


def main():
    turtle.setup(4096, 4096, -1024)
    with open("data/original_pulsars.json", "r") as f:
        pulsars = json.load(f)

    t = Turtle("blank")
    t.speed(0)

    t.forward(100 * WORLD_SCALE)
    t.right(90)
    t.forward(0.5 * WORLD_SCALE)
    t.right(180)
    t.forward(WORLD_SCALE)

    for pulsar in pulsars:
        t = Turtle("blank")
        t.speed(0)

        draw_star(t, pulsar)

    canvas = turtle.getscreen().getcanvas()
    canvas.postscript(file="pulsar.ps")

    img = Image.open("pulsar.ps")
    img = convert_to_rgba(img)
    img.save("pulsar.png", "PNG")


if __name__ == "__main__":
    main()
