import numpy
from scipy.optimize import fsolve
from drum_sensor.samples import convert_samples_to_seconds
from drum_sensor.quadrant import find_quadrant, convert_cross_samples_absolute


def _calculate_params(td_1, td_2, speed, distance):
    """docstring for calculate_params"""
    time_diff = abs(td_2 - td_1)
    my_a = speed * time_diff / 2
    my_c = distance / 2
    return ((1 / my_a**2), (1 / (my_c**2 - my_a**2)))


def _calculate_params_crosscorrelate(td, speed, distance):
    """docstring for calculate_params"""
    time_diff = abs(td)
    my_a = speed * time_diff / 2
    my_c = distance / 2
    return ((1 / my_a**2), (1 / (my_c**2 - my_a**2)))


# discovery function only used in tests
def convert_time_deltas(time_deltas_samples):
    return [
        (time_deltas_samples[1] - time_deltas_samples[0]),
        (time_deltas_samples[2] - time_deltas_samples[1]),
        (time_deltas_samples[3] - time_deltas_samples[2]),
        (time_deltas_samples[0] - time_deltas_samples[3]),
    ]


def generate_coefficients(time_deltas_samples, speed, distance):
    time_deltas_seconds = list(map(convert_samples_to_seconds, time_deltas_samples))

    quadrant, quadrant_starting_point = find_quadrant(time_deltas_seconds, distance)

    print(f"quadrant: {quadrant}")
    print(f"quadrant starting point: {quadrant_starting_point}")

    a, b = _calculate_params(
        time_deltas_seconds[0], time_deltas_seconds[1], speed, distance
    )
    c, d = _calculate_params(
        time_deltas_seconds[1], time_deltas_seconds[2], speed, distance
    )
    e, f = _calculate_params(
        time_deltas_seconds[2], time_deltas_seconds[3], speed, distance
    )
    g, h = _calculate_params(
        time_deltas_seconds[3], time_deltas_seconds[0], speed, distance
    )
    return (quadrant_starting_point, a, b, c, d, e, f, g, h)


def calculate_point(time_deltas_samples, speed, distance):
    quadrant_starting_point, a, b, c, d, e, f, g, h = generate_coefficients(
        time_deltas_samples, speed, distance
    )
    return calculate_point_coefficients(quadrant_starting_point, a, b, c, d, e, f, g, h)


def generate_coefficients_crosscorrelate(time_deltas_samples, speed, distance):
    time_deltas_seconds = list(map(convert_samples_to_seconds, time_deltas_samples))

    quadrant, quadrant_starting_point = find_quadrant(
        convert_cross_samples_absolute(time_deltas_seconds), distance
    )

    print(f"quadrant: {quadrant}")
    print(f"quadrant starting point: {quadrant_starting_point}")

    a, b = _calculate_params_crosscorrelate(time_deltas_seconds[0], speed, distance)
    c, d = _calculate_params_crosscorrelate(time_deltas_seconds[1], speed, distance)
    e, f = _calculate_params_crosscorrelate(time_deltas_seconds[2], speed, distance)
    g, h = _calculate_params_crosscorrelate(time_deltas_seconds[3], speed, distance)
    return (quadrant_starting_point, a, b, c, d, e, f, g, h)


def calculate_point_crosscorrelate(time_deltas_samples, speed, distance):
    (
        quadrant_starting_point,
        a,
        b,
        c,
        d,
        e,
        f,
        g,
        h,
    ) = generate_coefficients_crosscorrelate(time_deltas_samples, speed, distance)
    return calculate_point_coefficients(quadrant_starting_point, a, b, c, d, e, f, g, h)


def calculate_point_coefficients(quadrant_starting_point, a, b, c, d, e, f, g, h):
    print("equations:")
    print(f"NE ({a}x^2)-({b}(y-.1)^2)=1")
    print(f"ES ({c}y^2)-({d}(x-.1)^2)=1")
    print(f"SW ({e}x^2)-({f}(y+.1)^2)=1")
    print(f"WN ({g}y^2)-({h}(x+.1)^2)=1")

    def equations_1(vars):
        x, y = vars
        eqs = [
            (a * (x**2)) - (b * ((y - 0.1) ** 2)) - 1,
            (c * (y**2)) - (d * ((x - 0.1) ** 2)) - 1,
        ]
        return eqs

    def equations_2(vars):
        x, y = vars
        eqs = [
            (c * (y**2)) - (d * ((x - 0.1) ** 2)) - 1,
            (e * (x**2)) - (f * ((y + 0.1) ** 2)) - 1,
        ]
        return eqs

    def equations_3(vars):
        x, y = vars
        eqs = [
            (e * (x**2)) - (f * ((y + 0.1) ** 2)) - 1,
            (g * (y**2)) - (h * ((x + 0.1) ** 2)) - 1,
        ]
        return eqs

    def equations_4(vars):
        x, y = vars
        eqs = [
            (g * (y**2)) - (h * ((x + 0.1) ** 2)) - 1,
            (a * (x**2)) - (b * ((y - 0.1) ** 2)) - 1,
        ]
        return eqs

    solutions = []

    # attempt to solve pairs of equations
    solutions.append(fsolve(equations_1, quadrant_starting_point))
    solutions.append(fsolve(equations_2, quadrant_starting_point))
    solutions.append(fsolve(equations_3, quadrant_starting_point))
    solutions.append(fsolve(equations_4, quadrant_starting_point))

    print("intersections:")
    print(solutions)

    x, y = numpy.mean(solutions, axis=0)
    std_x, std_y = numpy.std(solutions, axis=0)

    print(f"predicted point: ({x}, {y})")
    print(f"std: ({std_x}, {std_y})")

    return (x, y, std_x, std_y)
