# this is a simple turtle script

from wrappers import Turtle

def draw(canvas):
    t = Turtle(canvas)
    t.cls()
    t.forward(100)
    t.write("Hello Turtle")
