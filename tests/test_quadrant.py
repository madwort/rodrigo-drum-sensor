from drum_sensor import quadrant

import pytest

testdata = [
    ([0, 80, 125, 83], [80, 45, -42, -83]),
    ([70, 117, 77, 0], [47, -40, -77, 70]),
    ([29, 30, 0, 31], [1, -30, 31, -2]),
]

midpoint_testdata = [
    ([0, 90, 90, 0], "north-west", (-0.0505, 0)),
    ([0, 0, 90, 90], "north-east", (0, 0.0505)),
    ([90, 90, 0, 0], "south-west", (0, -0.0505)),
    ([90, 0, 0, 90], "south-east", (0.0505, 0)),
    ([0, 0, 0, 0], "dead-centre", (0, 0)),
    ([0, 0, 0, 1], "dead-centre", (0, 0)),
]


def test__min_position():
    deltas = [80, 1, 125, 83]

    print(min(deltas))
    my_i = quadrant._min_position(deltas)
    print(my_i)
    assert my_i == [1]


def test__min_position_twin():
    deltas = [80, 1, 1, 125]

    print(min(deltas))
    my_i = quadrant._min_position(deltas)
    print(my_i)
    assert my_i == [1, 2]


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


@pytest.mark.parametrize(
    "time_deltas_samples,quadrant_name,starting_point", midpoint_testdata
)
def test_quadrant_midpoint(time_deltas_samples, quadrant_name, starting_point):
    deltas = time_deltas_samples

    my_quadrant, my_starting_position = quadrant.find_quadrant(deltas, 0.202)

    assert my_quadrant == quadrant_name
    assert my_starting_position == starting_point


def test_quadrant_crosscorrelate():
    # this should equal to [0, 80, 125, 83]
    deltas = [80, 45, -42, -83]

    my_quadrant, starting_position = quadrant.find_quadrant(
        quadrant.convert_cross_samples_absolute(deltas), 0.202
    )

    assert my_quadrant == "north"
    assert starting_position == (-0.0505, 0.0505)


@pytest.mark.parametrize("time_deltas_samples,time_deltas_samples_cross", testdata)
def test_quadrant_compare(time_deltas_samples, time_deltas_samples_cross):
    my_quadrant, starting_position = quadrant.find_quadrant(time_deltas_samples, 0.202)
    my_quadrant_cross, starting_position_cross = quadrant.find_quadrant(
        quadrant.convert_cross_samples_absolute(time_deltas_samples_cross), 0.202
    )

    assert my_quadrant == my_quadrant_cross
    assert starting_position == starting_position_cross


def test_convert_cross_samples_absolute():
    relative_deltas = [80, 45, -42, -83]
    absolute_deltas = quadrant.convert_cross_samples_absolute(relative_deltas)

    assert absolute_deltas == [0, 80, 125, 83]


@pytest.mark.parametrize("time_deltas_samples,time_deltas_samples_cross", testdata)
def test_convert_cross_samples_absolute(time_deltas_samples, time_deltas_samples_cross):
    relative_deltas = time_deltas_samples_cross
    absolute_deltas = quadrant.convert_cross_samples_absolute(relative_deltas)

    assert absolute_deltas == time_deltas_samples


def test_find_zero_crossings():
    crossings = quadrant.find_zero_crossings([80, 45, -42, -83])
    assert crossings == [0]


def test_find_zero_crossings_double():
    crossings = quadrant.find_zero_crossings([1, -30, 31, -2])
    assert crossings == [0, 2]


def test_find_zero_crossings_zero_1():
    crossings = quadrant.find_zero_crossings([0, -30, 0, 30])
    assert crossings == [2, 3]


def test_find_zero_crossings_none():
    # this was some actual generated test data, unclear what it means in the real world
    crossings = quadrant.find_zero_crossings([-1.5, -1.5, -1.5, -1.5])
    assert crossings == []
