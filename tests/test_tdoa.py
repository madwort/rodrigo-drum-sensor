from drum_sensor.tdoa import calculate_point

import numpy
import pytest

testdata = [
    ([0, 80, 125, 83], (-0.08199618647736903, 0.08692143585675399)),
    ([7, 4, 0, 4], (0.004566751345874217, -0.0045667513458737))
]

@pytest.mark.parametrize("time_deltas_samples,expected_point", testdata)
def test_calculate_point(time_deltas_samples, expected_point):
    speed = 82

    #  in m
    distance = 0.202

    x, y = calculate_point(time_deltas_samples, speed, distance)

    expected_x, expected_y = expected_point
    assert numpy.isclose(x,expected_x)
    assert numpy.isclose(y,expected_y)

