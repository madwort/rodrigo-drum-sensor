
from scipy.optimize import fsolve

print("equations:")
print("NE (148x^2)-(305(y-.1)^2)=1")
print("ES (540y^2)-(122(x-.1)^2)=1")
print("SW (493x^2)-(125(y+.1)^2)=1")
print("WN (156y^2)-(227(x+.1)^2)=1")

def equations_1(vars):
    x,y = vars
    eqs = [(148*(x**2))-(305*((y-.1)**2))-1, (540*(y**2))-(122*((x-.1)**2))-1]
    return eqs

def equations_2(vars):
    x,y = vars
    eqs = [(540*(y**2))-(122*((x-.1)**2))-1, (493*(x**2))-(125*((y+.1)**2))-1]
    return eqs

def equations_3(vars):
    x,y = vars
    eqs = [(493*(x**2))-(125*((y+.1)**2))-1, (156*(y**2))-(227*((x+.1)**2))-1]
    return eqs

def equations_4(vars):
    x,y = vars
    eqs = [(156*(y**2))-(227*((x+.1)**2))-1, (148*(x**2))-(305*((y-.1)**2))-1]
    return eqs

# attempt to solve pairs of equations

# first pair have a good soln at (-0.0823, 0.0968), a near soln at (0.1153, 0.0436) & two other far solns...

# we only want solutions in the upper-left quadrant, so seed the solver with a midpoint of that quadrant (outer corner of that quadrant may be a better choice - testing required)

quadrant_starting_point = (-0.05,0.05)
print(f"quadrant starting point: {quadrant_starting_point}")

print("intersections:")
x1,y1 = fsolve(equations_1, quadrant_starting_point)
print(x1,y1)
x2,y2 = fsolve(equations_2, quadrant_starting_point)
print(x2,y2)
x3,y3 = fsolve(equations_3, quadrant_starting_point)
print(x3,y3)
x4,y4 = fsolve(equations_4, quadrant_starting_point)
print(x4,y4)

x = (x1+x2+x3+x4)/4
y = (y1+y2+y3+y4)/4
print("predicted point:")
print(x,y)
