from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from drum_sensor.tdoa import calculate_point


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

    time_deltas_samples = args
    print(f"time deltas: {time_deltas_samples}")

    speed = 82
    print(f"speed: {speed}m/s")

    #  in m
    distance = 0.202
    print(f"sensor-to-sensor distance: {distance}")

    x, y, std_x, std_y = calculate_point(time_deltas_samples, speed, distance)

    print(f"predicted point: ({x}, {y})")
    print(f"std: ({std_x}, {std_y})")


dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever
