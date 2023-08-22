from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from drum_sensor.tdoa import calculate_point_crosscorrelate


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

    time_deltas_samples = args
    print(f"time deltas: {time_deltas_samples}")

    speed = 82
    print(f"speed: {speed}m/s")

    #  in m
    distance = 0.202
    print(f"sensor-to-sensor distance: {distance}m")

    x, y, std_x, std_y = calculate_point_crosscorrelate(
        time_deltas_samples, speed, distance
    )

    print(f"predicted point: ({x}, {y})")
    print(f"std: ({std_x}, {std_y})")

    # TODO: don't do this in the handler ARGH!
    client_ip = "127.0.0.1"
    client_port = 1338
    client_url = "/drum_sensor/calculated_point"

    print(f"sending OSC message to {client_ip}:{client_port}{client_url}")

    client = SimpleUDPClient(client_ip, client_port)  # Create client
    client.send_message("/drum_sensor/calculated_point", [x, y, std_x, std_y])


dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever
