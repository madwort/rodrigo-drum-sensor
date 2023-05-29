deltas = [80, 1, 125, 83]

def min_position(my_list):
    """docstring for min_position"""
    my_min = min(my_list)
    for i,x in enumerate(deltas):
        if x == my_min:
            return i

print(min(deltas))
print(min_position(deltas))
