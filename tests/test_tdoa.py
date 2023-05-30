from drum_sensor.tdoa import calculate_point

import numpy

def test_calculate_point():
    time_deltas_samples = [0, 80, 125, 83]

    speed = 82

    #  in m
    distance = 0.202

    x, y = calculate_point(time_deltas_samples, speed, distance)

    assert numpy.isclose(x,-0.08199618647736903)
    assert numpy.isclose(y,0.08692143585675399)

