deltas = [80, 1, 125, 83]

def _min_position(my_list):
    """docstring for min_position"""
    my_min = min(my_list)
    for i,x in enumerate(deltas):
        if x == my_min:
            # take the first among equals position
            # TODO: do something more clever if there are multiple equal min positions
            return i

def find_quadrant(my_list):
    quadrants = ["north", "east", "south", "west"]
    starting_positions = [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]

    posn = _min_position(my_list)
    return (quadrants[posn], starting_positions[posn])

quadrant, starting_position = find_quadrant(deltas)

print(min(deltas))
my_i = _min_position(deltas)
print(my_i)
print(f"{quadrant} quadrant")
print(f"starting position: {starting_position}")
