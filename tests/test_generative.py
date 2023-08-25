from drum_sensor.tdoa import (
    calculate_point,
)
from drum_sensor.samples import convert_seconds_to_samples
import math
import pytest

distance = [0.202]


def _generate_test_positions(distances):
    distance = distances[0]
    test_positions = []
    count = 10
    corner = -distance / 2
    spacing = distance / count
    for x in range(count):
        for y in range(count):
            test_positions.append(((corner + (spacing * x)), (corner + (spacing * y))))
    return test_positions


test_positions = _generate_test_positions(distance)


def _diagonal_distance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    distance = math.sqrt((x**2) + (y**2))
    return distance


def _generate_tdoa_from_point(test_point, speed, distance):
    time_deltas_samples = []
    sensor_positions = [
        (-distance / 2, distance / 2),
        (distance / 2, distance / 2),
        (distance / 2, -distance / 2),
        (-distance / 2, -distance / 2),
    ]
    for sensor_position in sensor_positions:
        time_deltas_samples.append(
            convert_seconds_to_samples(
                _diagonal_distance(test_point, sensor_position) / speed
            )
        )

    return time_deltas_samples


@pytest.mark.parametrize("distance", distance)
@pytest.mark.parametrize("test_point", test_positions)
def test_calculate_point_batch(distance, test_point):
    speed = 82

    #  in m
    # distance = 0.202

    # test_point = (0.05, 0.05)
    time_deltas_samples = _generate_tdoa_from_point(test_point, speed, distance)

    x, y, std_x, std_y = calculate_point(time_deltas_samples, speed, distance)

    error = _diagonal_distance((x, y), test_point)

    print("-------------------------------------------")
    print(f"test point: {test_point}")
    print(f"time deltas: {time_deltas_samples}")
    print(f"calculated point: {x},{y}")
    print(f"error: {error}")
    print("-------------------------------------------")

    assert error < 0.0005