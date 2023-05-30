from drum_sensor.tdoa import calculate_point

time_deltas_samples = [0, 80, 125, 83]
# time_deltas_samples = [7, 4, 0, 4]
print(f"time deltas: {time_deltas_samples}")

speed = 82
print(f"speed: {speed}m/s")

#  in m
distance = 0.202
print(f"sensor-to-sensor distance: {distance}")

x, y = calculate_point(time_deltas_samples, speed, distance)

print("predicted point:")
print(x, y)
