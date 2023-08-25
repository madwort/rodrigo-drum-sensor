from drum_sensor.tdoa import (
    calculate_point,
)
from drum_sensor.samples import convert_seconds_to_samples
from drum_sensor.quadrant import get_fudge_factor
import math


import csv


def main():
    csvfile = open("error.csv", "w", newline="")
    spamwriter = csv.writer(
        csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )

    distance = 0.202
    count = 15
    # TODO: remove fudge factor because it crashes at the extreme edges
    corner = (-distance / 2) + 0.0001
    spacing = distance / count
    total_error = 0
    worst_error = 0
    header_row = ["x"]
    for y in range(count):
        header_row.append((corner + (spacing * y)))
    spamwriter.writerow(header_row)

    for x in range(count):
        my_row = [(corner + (spacing * x))]
        for y in range(count):
            my_error = test_calculate_point(
                distance, ((corner + (spacing * x)), (corner + (spacing * y)))
            )
            my_row.append(my_error)
            total_error += my_error
            if my_error > worst_error:
                worst_error = my_error
        spamwriter.writerow(my_row)

    spamwriter.writerow([])
    spamwriter.writerow(["fudge factor",f"{get_fudge_factor()}"])
    spamwriter.writerow(["sample points",f"{count**2}"])
    spamwriter.writerow(["total error",f"{total_error}"])
    spamwriter.writerow(["mean error",f"{total_error/(count**2)}"])
    spamwriter.writerow(["worst error",f"{worst_error}"])

    print("===========================================")
    print(f"fudge factor: {get_fudge_factor()}")
    print(f"sample points: {count**2}")
    print(f"total error: {total_error}")
    print(f"mean error: {total_error/(count**2)}")
    print(f"worst error: {worst_error}")
    print("===========================================")


def _diagonal_distance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    distance = math.sqrt((x**2) + (y**2))
    return distance


def _generate_tdoa_from_point(test_point, speed, distance):
    time_deltas_samples = []
    sensor_positions = [
        (-distance / 2, distance / 2),
        (distance / 2, distance / 2),
        (distance / 2, -distance / 2),
        (-distance / 2, -distance / 2),
    ]
    for sensor_position in sensor_positions:
        time_deltas_samples.append(
            convert_seconds_to_samples(
                _diagonal_distance(test_point, sensor_position) / speed
            )
        )

    return time_deltas_samples


def test_calculate_point(distance, test_point):
    # TODO: get this to output a CSV & then make a graphing pipeline
    # ...and then improve the performance!
    speed = 82

    #  in m
    # distance = 0.202

    # test_point = (0.05, 0.05)
    time_deltas_samples = _generate_tdoa_from_point(test_point, speed, distance)

    x, y, std_x, std_y = calculate_point(time_deltas_samples, speed, distance)

    error = _diagonal_distance((x, y), test_point)

    print("-------------------------------------------")
    print(f"test point: {test_point}")
    print(f"time deltas: {time_deltas_samples}")
    print(f"calculated point: {x},{y}")
    print(f"error: {error}")
    print("-------------------------------------------")
    return error


if __name__ == "__main__":
    main()
