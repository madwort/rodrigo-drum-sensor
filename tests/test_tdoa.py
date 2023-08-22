from drum_sensor.tdoa import (
    calculate_point,
    calculate_point_crosscorrelate,
    generate_coefficients,
    generate_coefficients_crosscorrelate,
)

import numpy
import pytest

testdata = [
    (
        [0, 80, 125, 83],
        (-0.08199618647736903, 0.08692143585675399),
        (0.006395308834651672, 0.006828757223941415),
    ),
    (
        [7, 4, 0, 4],
        (0.004566751345874217, -0.0045667513458737),
        (0.0005514049304094885, 0.0005514049304090638),
    ),
    (
        [0, 82, 136, 82],
        (-0.10623391246350365, 0.10623391246351387),
        (0.030940759000152925, 0.030940759000144185),
    ),
    (
        [0, 77, 124, 81],
        (-0.08218499505826882, 0.08871530707404185),
        (0.00990158369200529, 0.010704979806424278),
    ),
    (
        [81, 0, 79, 117],
        (0.07723815321925999, 0.07392248026592782),
        (0.003624558160108827, 0.003511846510005707),
    ),
    (
        [90, 0, 90, 124],
        (0.07832980953338092, 0.07832980953338092),
        (0.012415343915888867, 0.012415343915888867),
    ),
    (
        [77, 0, 81, 120],
        (0.0765109989247526, 0.08304274142552162),
        (0.0030041510963897703, 0.003283378859201837),
    ),
    (
        [133, 82, 0, 82],
        (0.09840269371389346, -0.09840269371532345),
        (0.0224956927850102, 0.022495692787188656),
    ),
    (
        [119, 87, 0, 91],
        (0.0785261993011436, -0.07098095162190782),
        (0.019246954133567223, 0.017297146434860224),
    ),
    (
        [117, 89, 0, 91],
        (0.07533891044074259, -0.07136379917418237),
        (0.023946112691366265, 0.022613862465255288),
    ),
    (
        [83, 135, 87, 0],
        (-0.10126799320721791, -0.09458298914842288),
        (0.01969107563898766, 0.01798902955487899),
    ),
    (
        [86, 136, 87, 0],
        (-0.09840541965966135, -0.09673892198645997),
        (0.01736681004919172, 0.016954451633795754),
    ),
    (
        [70, 117, 77, 0],
        (-0.08603283412602358, -0.07478580908218872),
        (0.009982940470821529, 0.008864968087728535),
    ),
    (
        [87, 106, 36, 0],
        (-0.0392633947602687, -0.12557977453066305),
        (0.004837576414917338, 0.010335475412393918),
    ),
    (
        [88, 23, 0, 74],
        (0.10498233546958241, -0.025556539981573347),
        (0.007440531279096527, 0.004204461519220093),
    ),
    (
        [74, 60, 0, 37],
        (0.03090160796349531, -0.0653344477688675),
        (0.005821057794036138, 0.007082238385153403),
    ),
    (
        [65, 8, 0, 83],
        (0.041761469703860465, -0.025412289298273678),
        (0.0959625249688967, 0.013137950206507062),
    ),
    (
        [0, 17, 80, 70],
        (-0.01820749716817085, 0.09879170527924472),
        (0.0024162853667972746, 0.004120533014859691),
    ),
    (
        [15, 0, 60, 66],
        (0.012801872756658082, 0.07836258890834677),
        (0.0014703501335117033, 0.0020328893482624154),
    ),
    (
        [29, 30, 0, 31],
        (0.01965685354327838, -0.01977876469592925),
        (0.01831626060232068, 0.017007225390593017),
    ),
    (
        [29, 30, 0, 31],
        (0.01965685354327838, -0.01977876469592925),
        (0.01831626060232068, 0.017007225390593017),
    ),
    (
        [64, 64, 1, 0],
        (-0.0007351120602235915, -0.0005526554366400843),
        (0.0008271354253725052, 0.09329069005179348),
    ),
    (
        [76, 110, 69, 0],
        (-0.06663724261388546, -0.07785863617548007),
        (4.7146824482418955e-05, 2.5704656876176696e-05),
    ),
]


def _compare_points(calculated_point, calculated_std, expected_point, expected_std):
    x, y = calculated_point
    std_x, std_y = calculated_std
    expected_x, expected_y = expected_point
    expected_std_x, expected_std_y = expected_std
    assert numpy.isclose(x, expected_x)
    assert numpy.isclose(y, expected_y)
    assert numpy.isclose(std_x, expected_std_x)
    assert numpy.isclose(std_y, expected_std_y)


@pytest.mark.parametrize("time_deltas_samples,expected_point,expected_std", testdata)
def test_calculate_point(time_deltas_samples, expected_point, expected_std):
    speed = 82

    #  in m
    distance = 0.202

    print(f"time deltas: {time_deltas_samples}")
    x, y, std_x, std_y = calculate_point(time_deltas_samples, speed, distance)

    _compare_points((x, y), (std_x, std_y), expected_point, expected_std)


@pytest.mark.parametrize("time_deltas_samples,expected_point,expected_std", testdata)
def test_calculate_point_crosscorrelate(
    time_deltas_samples, expected_point, expected_std
):
    speed = 82

    #  in m
    distance = 0.202

    print(f"time deltas: {time_deltas_samples}")
    relative_time_deltas_samples = convert_time_deltas(time_deltas_samples)
    print(f"time deltas (relative): {relative_time_deltas_samples}")
    x, y, std_x, std_y = calculate_point_crosscorrelate(
        relative_time_deltas_samples, speed, distance
    )

    _compare_points((x, y), (std_x, std_y), expected_point, expected_std)


def convert_time_deltas(time_deltas_samples):
    return [
        (time_deltas_samples[1] - time_deltas_samples[0]),
        (time_deltas_samples[2] - time_deltas_samples[1]),
        (time_deltas_samples[3] - time_deltas_samples[2]),
        (time_deltas_samples[0] - time_deltas_samples[3]),
    ]


@pytest.mark.parametrize("time_deltas_samples,expected_point,expected_std", testdata)
def test_convert_time_deltas(time_deltas_samples, expected_point, expected_std):
    print(time_deltas_samples)
    newstyle = convert_time_deltas(time_deltas_samples)
    print(newstyle)
    assert sum(newstyle) == 0


def test_generate_coefficients():
    speed = 82

    #  in m
    distance = 0.202

    regular = generate_coefficients([0, 80, 125, 83], speed, distance)
    new = generate_coefficients_crosscorrelate([80, 45, -42, -83], speed, distance)

    # test first param with equality, this is the quadrant tuple
    assert regular[0] == new[0]

    # test the other params are close, as they are floats
    for i in range(1, len(regular) - 1):
        assert numpy.isclose(regular[i], new[i])


def test_generate_coefficients_2():
    # two adjacent equal times
    speed = 82

    #  in m
    distance = 0.202

    regular = generate_coefficients([0, 80, 80, 125], speed, distance)

    assert regular == (
        (-0.0505, 0.0505),
        180.7713042831648,
        214.1718103968868,
        5948839976204.641,
        98.02960494230749,
        571.3265913146938,
        118.33356571265956,
        74.0439262343843,
        -302.6179465626542,
    )
