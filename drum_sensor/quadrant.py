def _min_position(my_list):
    """docstring for min_position"""
    my_min = min(my_list)
    for i, x in enumerate(my_list):
        if x == my_min:
            # take the first among equals position
            # TODO: do something more clever if there are multiple equal min positions
            return i


def find_quadrant(my_list, distance):
    quadrants = ["north", "east", "south", "west"]
    # rough midpoint of the quadrant
    midpoint = distance / 4
    # if there are multiple equal points, we may want to do e.g. (midpoint, 0)
    starting_positions = [
        (-midpoint, midpoint),
        (midpoint, midpoint),
        (midpoint, -midpoint),
        (-midpoint, -midpoint),
    ]

    posn = _min_position(my_list)
    return (quadrants[posn], starting_positions[posn])
