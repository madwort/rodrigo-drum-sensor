from drum_sensor.samples import convert_seconds_to_samples, convert_samples_to_seconds

import csv
import math
import numpy
import matplotlib.pyplot as plt


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


def main():
    csvfile = open("mapping.csv", "w", newline="")
    spamwriter = csv.writer(
        csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )

    speed = 82
    distance = 0.202
    count = 50
    # TODO: remove fudge factor because it crashes at the extreme edges
    corner = (-distance / 2) + 0.00001
    spacing = distance / count
    total_error = 0
    worst_error = 0
    header_row = ["x"]
    for y in range(count):
        header_row.append((corner + (spacing * y)))
    spamwriter.writerow(header_row)
    results_array = []

    for x in range(count):
        row_results = []
        my_row = [(corner + (spacing * x))]
        for y in range(count):
            point = ((corner + (spacing * x)), (corner + (spacing * y)))
            my_tdoa = _generate_tdoa_from_point(point, speed, distance)
            ptp_size = numpy.ptp(my_tdoa)
            print(f"{point} - {my_tdoa} - {convert_samples_to_seconds(ptp_size)}")
            my_row.append(convert_samples_to_seconds(ptp_size))
            row_results.append(convert_samples_to_seconds(ptp_size))
        spamwriter.writerow(my_row)
        results_array.append(row_results)

    mynumpy = numpy.array(results_array)
    fig, ax = plt.subplots()
    ax.imshow(mynumpy)
    plt.show()


if __name__ == "__main__":
    main()
