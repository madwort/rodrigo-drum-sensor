def get_fudge_factor():
    return 0.0002


def _min_position(my_list):
    """docstring for min_position"""
    my_min = min(my_list)
    fudge_factor = get_fudge_factor()
    min_indices = [i for i, x in enumerate(my_list) if x <= (my_min + fudge_factor)]
    return min_indices


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

    min_posns = _min_position(my_list)

    print(f"min_posns: {min_posns}")

    # default quadrant (assuming one minimum)
    posn = min_posns[0]
    quadrant_name = quadrants[posn]
    starting_position = starting_positions[posn]

    if len(min_posns) == 2:
        if min_posns[0] == 1 and min_posns[1] == 2:
            # fixup for SE
            quadrant_name = f"{quadrants[min_posns[1]]}-{quadrants[min_posns[0]]}"
        else:
            quadrant_name = f"{quadrants[min_posns[0]]}-{quadrants[min_posns[1]]}"
        starting_position = (
            (starting_positions[min_posns[0]][0] + starting_positions[min_posns[1]][0])
            / 2,
            (starting_positions[min_posns[0]][1] + starting_positions[min_posns[1]][1])
            / 2,
        )

    if len(min_posns) >= 3:
        # three equal minimums is theoretically impossible, but happens in practice due to
        # noisy measurements, though it's most likely a noisy dead-centre hit, so just do that
        quadrant_name = "dead-centre"
        starting_position = (0, 0)

    return (quadrant_name, starting_position)


def find_zero_crossings(my_list):
    """can return 0,1 or 2 indices of crossings"""
    crossings = []
    for i, x in enumerate(my_list):
        if x >= 0 and my_list[(i - 1) % len(my_list)] <= 0:
            crossings.append(i)
    return crossings


def convert_cross_samples_absolute(my_list):
    crossings = find_zero_crossings(my_list)
    zero_index = 0
    if len(crossings) == 0:
        # TODO: try  normalising the samples to see if we can improve on this
        # needs real-world test data tho
        print("Warning - No zero crossings, arbitrarily sticking with [0].")
    else:
        # default to the first crossing, this should be 0
        zero_index = crossings[0]

    # unless there are two crossings, in which case take the larger of the two
    if len(crossings) == 2:
        if my_list[crossings[1]] > my_list[crossings[0]]:
            zero_index = crossings[1]

    absolute_list = [0] * len(my_list)

    for i in range(1, len(my_list)):
        target_index = (zero_index + i) % len(my_list)
        source_index = (target_index - 1) % len(my_list)
        absolute_list[target_index] = (
            absolute_list[source_index] + my_list[source_index]
        )

    print(f"absolute_list: {absolute_list}")
    return absolute_list


def find_quadrant_cross(my_list, distance):
    my_list_absolute = convert_cross_samples_absolute(my_list)
    return find_quadrant(my_list_absolute, distance)
