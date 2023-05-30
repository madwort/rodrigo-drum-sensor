from drum_sensor import quadrant

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

    