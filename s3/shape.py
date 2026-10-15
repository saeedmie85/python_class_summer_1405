import turtle
import random
t = turtle.Turtle()
colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "purple",
    "pink",
    "brown",
    "black",
    "white",
    "gray",
    "cyan",
    "magenta",
    "gold",
    "silver",
    "lime",
    "navy",
    "violet",
    "coral",
    "turquoise"
]

t.speed(-1)

f = 300
for i in range(100):
    t.pencolor(random.choice(colors))
    for _ in range(4):
        t.forward(200)
        t.left(90)
    t.left(3.6)


