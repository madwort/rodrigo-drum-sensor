from drum_sensor import quadrant

import pytest

testdata = [
    ([0, 80, 125, 83], [80, 45, -42, -83]),
    ([70, 117, 77, 0], [47, -40, -77, 70]),
]


def test__min_position():
    deltas = [80, 1, 125, 83]

    print(min(deltas))
    my_i = quadrant._min_position(deltas)
    print(my_i)
    assert my_i == 1


def test_quadrant():
    deltas = [80, 1, 125, 83]

    my_quadrant, starting_position = quadrant.find_quadrant(deltas, 0.202)

    assert my_quadrant == "east"
    assert starting_position == (0.0505, 0.0505)


def test_quadrant_2():
    deltas = [0, 80, 125, 83]

    my_quadrant, starting_position = quadrant.find_quadrant(deltas, 0.202)

    assert my_quadrant == "north"
    assert starting_position == (-0.0505, 0.0505)


def test_quadrant_crosscorrelate():
    # this should equal to [0, 80, 125, 83]
    deltas = [80, 45, -42, -83]

    my_quadrant, starting_position = quadrant.find_quadrant(deltas, 0.202)

    assert my_quadrant == "north"
    assert starting_position == (-0.0505, 0.0505)


@pytest.mark.parametrize("time_deltas_samples,time_deltas_samples_cross", testdata)
def test_quadrant_compare(time_deltas_samples, time_deltas_samples_cross):
    my_quadrant, starting_position = quadrant.find_quadrant(time_deltas_samples, 0.202)
    my_quadrant_cross, starting_position_cross = quadrant.find_quadrant(
        time_deltas_samples_cross, 0.202
    )

    assert my_quadrant == my_quadrant_cross
    assert starting_position == starting_position_cross
