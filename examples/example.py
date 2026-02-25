from sympy_desmos import Desmos2D, Desmos3D
from sympy import *
from sympy import Function as F


x, y, z = symbols("x y z")


desmos = Desmos2D()


desmos.write([(1,2), (3,4), (5,6)]) # list of points
desmos.write(x ** 2) # x^2
desmos.write(Matrix([1,0.5])) # (1,1)

def drawline(v1, v2, t):
    return v1 + t * (v2 - v1)

t = symbols("t")
p1 = Matrix([0,1])
p2 = Matrix([1,1])
desmos.write("p_1", p1)
desmos.write("p_2", p2, color="cyan")


desmos.open_browser()


