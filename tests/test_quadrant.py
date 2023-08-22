from drum_sensor import quadrant

import pytest

conversion_testdata = [
    ([0, 80, 125, 83], [80, 45, -42, -83]),
    ([70, 117, 77, 0], [47, -40, -77, 70]),
    ([29, 30, 0, 31], [1, -30, 31, -2]),
    ([0, 66, 68, 3], [66, 2, -65, -3]),
    ([10, 2, 0, 7], [-8, -2, 7, 3]),
]

quadrant_testdata = [
    ([80, 1, 125, 83], "east", (0.0505, 0.0505)),
    ([0, 80, 125, 83], "north", (-0.0505, 0.0505)),
]

midpoint_testdata = [
    ([0, 90, 90, 0], "north-west", (-0.0505, 0)),
    ([0, 0, 90, 90], "north-east", (0, 0.0505)),
    ([90, 90, 0, 0], "south-west", (0, -0.0505)),
    ([90, 0, 0, 90], "south-east", (0.0505, 0)),
    ([0, 0, 0, 0], "dead-centre", (0, 0)),
    ([0, 0, 0, 1], "dead-centre", (0, 0)),
    ([64, 64, 1, 0], "west", (-0.0505, -0.0505)),
]

crossings_testdata = [
    ([80, 45, -42, -83], [0]),
    ([1, -30, 31, -2], [0, 2]),
    ([0, -30, 0, 30], [2, 3]),
    ([-1.5, -1.5, -1.5, -1.5], []),
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


@pytest.mark.parametrize(
    "time_deltas_samples,quadrant_name,starting_point", midpoint_testdata
)
def test_quadrant(time_deltas_samples, quadrant_name, starting_point):
    my_quadrant, my_starting_position = quadrant.find_quadrant(
        time_deltas_samples, 0.202
    )

    assert my_quadrant == quadrant_name
    assert my_starting_position == starting_point


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


@pytest.mark.parametrize(
    "time_deltas_samples,time_deltas_samples_cross", conversion_testdata
)
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


def test_convert_cross_samples_absolute2():
    relative_deltas = [0, -63, -1, 64]
    absolute_deltas = quadrant.convert_cross_samples_absolute(relative_deltas)

    assert absolute_deltas == [64, 64, 1, 0]


@pytest.mark.parametrize(
    "time_deltas_samples,time_deltas_samples_cross", conversion_testdata
)
def test_convert_cross_samples_absolute(time_deltas_samples, time_deltas_samples_cross):
    relative_deltas = time_deltas_samples_cross
    absolute_deltas = quadrant.convert_cross_samples_absolute(relative_deltas)

    assert absolute_deltas == time_deltas_samples


@pytest.mark.parametrize("time_deltas,crossings", crossings_testdata)
def test_find_zero_crossings(time_deltas, crossings):
    my_crossings = quadrant.find_zero_crossings(time_deltas)
    assert my_crossings == crossings
