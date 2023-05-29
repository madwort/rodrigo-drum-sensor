from sympy import solve

from sympy.abc import x, y

# equations:

# NE (148x^2)-(305(y-.1)^2)=1
# ES (540y^2)-(122(x-.1)^2)=1
# SW (493x^2)-(125(y+.1)^2)=1
# WN (156y^2)-(227(x+.1)^2)=1

# first pair have a good soln at (-0.0823, 0.0968), a near soln at (0.1153, 0.0436) & two other far solns...

equations = [(148*(x**2))-(305*((y-.1)**2))-1, (540*(y**2))-(122*((x-.1)**2))-1, (493*(x**2))-(125*((y+.1)**2))-1, (156*(y**2))-(227*((x+.1)**2))-1]

# attempt to solve pairs of equations

for x in range(0, 4):
    print(f"pair {x}")
    equation_1 = equations[x]
    if x < 3:
        equation_2 = equations[x+1]
    else:
        equation_2 = equations[0]
    try:
        solution = solve([equation_1, equation_2], x, y, dict=True)
        print(solution)
        print((x,y))
    except Exception:
        print("could not solve")
