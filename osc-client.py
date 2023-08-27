from pythonosc.udp_client import SimpleUDPClient


def main():
    """simulate Max sending a set of time offsets"""
    ip = "127.0.0.1"
    port = 1337

    client = SimpleUDPClient(ip, port)  # Create client

    client.send_message(
        "/drum_sensor/time_offsets", [-76.610723, -81.852569, 78.486943, 76.451051]
    )
    # client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string


if __name__ == "__main__":
    main()
