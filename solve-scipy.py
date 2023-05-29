
from scipy.optimize import fsolve

# equations:

# NE (148x^2)-(305(y-.1)^2)=1
# ES (540y^2)-(122(x-.1)^2)=1
# SW (493x^2)-(125(y+.1)^2)=1
# WN (156y^2)-(227(x+.1)^2)=1

def equations(vars):
    x,y = vars
    eqs = [(148*(x**2))-(305*((y-.1)**2))-1, (540*(y**2))-(122*((x-.1)**2))-1]
    return eqs

# attempt to solve pairs of equations

# first pair have a good soln at (-0.0823, 0.0968), a near soln at (0.1153, 0.0436) & two other far solns...

# we only want solutions in the upper-left quadrant, so seed the solver with a midpoint of that quadrant (outer corner of that quadrant may be a better choice - testing required)
x,y = fsolve(equations, (-0.05,0.05))
print((x,y))

