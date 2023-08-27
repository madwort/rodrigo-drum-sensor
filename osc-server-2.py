from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


def main():
    """simulate Max receiving a predicted set of coordinates"""
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(default_handler)

    ip = "127.0.0.1"
    port = 1338

    server = BlockingOSCUDPServer((ip, port), dispatcher)
    server.serve_forever()  # Blocks forever

if __name__ == "__main__":
    main()

