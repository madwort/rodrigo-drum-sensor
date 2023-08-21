from drum_sensor.tdoa import calculate_point_crosscorrelate

# time_deltas_samples = [0, 80, 125, 83]
# time_deltas_samples = [7, 4, 0, 4]
# time_deltas_samples = [-76.610723, -81.852569, 78.486943, 76.451051]
time_deltas_samples = [-38.251286, -35.28295, 40.369278, 41.334574]

print(f"time deltas: {time_deltas_samples}")

speed = 82
print(f"speed: {speed}m/s")

#  in m
distance = 0.202
print(f"sensor-to-sensor distance: {distance}")

x, y, std_x, std_y = calculate_point_crosscorrelate(time_deltas_samples, speed, distance)

print(f"predicted point: ({x}, {y})")
print(f"std: ({std_x}, {std_y})")
