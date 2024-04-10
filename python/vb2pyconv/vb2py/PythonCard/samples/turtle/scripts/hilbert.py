# example derived from
# Turtle Geometry: The Computer as a Medium for Exploring Mathematics
# by Harold Abelson and Andrea diSessa
# p. 96-98

from wrappers import CurvesTurtle

def draw(canvas):
    t = CurvesTurtle(canvas)
    t.cls()
    t.moveTo(50, 50)
    t.right(90)
    t.hilbert(5, 6, 1)
