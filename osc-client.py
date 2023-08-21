from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 1337

client = SimpleUDPClient(ip, port)  # Create client

client.send_message("/drum_sensor/server", [0, 80, 125, 83])
# client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string
