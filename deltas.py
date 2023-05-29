deltas = [80, 1, 125, 83]
quadrants = ["north", "east", "south", "west"]
starting_positions = [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]

def min_position(my_list):
    """docstring for min_position"""
    my_min = min(my_list)
    for i,x in enumerate(deltas):
        if x == my_min:
            return i

print(min(deltas))
my_i = min_position(deltas)
print(my_i)
print(f"{quadrants[my_i]} quadrant")
print(f"starting position: {starting_positions[my_i]}")
