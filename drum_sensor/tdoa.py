from scipy.optimize import fsolve
from drum_sensor.samples import convert_samples_to_seconds
from drum_sensor.quadrant import find_quadrant

def _calculate_params(td_1, td_2, speed, distance):
    """docstring for calculate_params"""
    time_diff = abs(td_2-td_1)
    my_a = speed*time_diff/2
    my_c = distance/2
    return ((1/my_a**2),(1/(my_c**2-my_a**2)))


def calculate_point(time_deltas_samples, speed, distance):
    time_deltas_seconds = list(map(convert_samples_to_seconds, time_deltas_samples))

    quadrant, quadrant_starting_point = find_quadrant(time_deltas_seconds, distance)

    a, b = _calculate_params(time_deltas_seconds[0], time_deltas_seconds[1], speed, distance)
    c, d = _calculate_params(time_deltas_seconds[1], time_deltas_seconds[2], speed, distance)
    e, f = _calculate_params(time_deltas_seconds[2], time_deltas_seconds[3], speed, distance)
    g, h = _calculate_params(time_deltas_seconds[3], time_deltas_seconds[0], speed, distance)

    print("equations:")
    print(f"NE ({a}x^2)-({b}(y-.1)^2)=1")
    print(f"ES ({c}y^2)-({d}(x-.1)^2)=1")
    print(f"SW ({e}x^2)-({f}(y+.1)^2)=1")
    print(f"WN ({g}y^2)-({h}(x+.1)^2)=1")

    def equations_1(vars):
        x,y = vars
        eqs = [(a*(x**2))-(b*((y-.1)**2))-1, (c*(y**2))-(d*((x-.1)**2))-1]
        return eqs

    def equations_2(vars):
        x,y = vars
        eqs = [(c*(y**2))-(d*((x-.1)**2))-1, (e*(x**2))-(f*((y+.1)**2))-1]
        return eqs

    def equations_3(vars):
        x,y = vars
        eqs = [(e*(x**2))-(f*((y+.1)**2))-1, (g*(y**2))-(h*((x+.1)**2))-1]
        return eqs

    def equations_4(vars):
        x,y = vars
        eqs = [(g*(y**2))-(h*((x+.1)**2))-1, (a*(x**2))-(b*((y-.1)**2))-1]
        return eqs

    # attempt to solve pairs of equations

    print(f"quadrant: {quadrant}")
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
    print(f"sumx {(x1+x2+x3)}")
    y = (y1+y2+y3+y4)/4
    print(x,y)
    return (x, y)

