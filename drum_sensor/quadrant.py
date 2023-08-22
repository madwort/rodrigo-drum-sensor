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


def find_zero_crossings(my_list):
    """can return 0,1 or 2 indices of crossings"""
    crossings = []
    for i, x in enumerate(my_list):
        if x > 0 and my_list[(i - 1) % len(my_list)] < 0:
            crossings.append(i)
    print(crossings)
    return crossings


def convert_cross_samples_absolute(my_list):
    # I think the position where the sign changes from neg to pos is the one
    # unless there are two, in which case the larger

    crossings = find_zero_crossings(my_list)
    if len(crossings) == 0:
        raise ValueError("No zero crossings, please normalise the samples.")

    if len(crossings) == 2:
        raise ValueError("Two zero crossings, please pick one.")

    zero_index = crossings[0]

    absolute_list = [0] * len(my_list)

    for i in range(1, len(my_list)):
        target_index = (zero_index + i) % len(my_list)
        print(target_index)
        source_index = (target_index - 1) % len(my_list)
        absolute_list[target_index] = (
            absolute_list[source_index] + my_list[source_index]
        )

    return absolute_list


def find_quadrant_cross(my_list, distance):
    my_list_absolute = convert_cross_samples_absolute(my_list)
    return find_quadrant(my_list_absolute, distance)
