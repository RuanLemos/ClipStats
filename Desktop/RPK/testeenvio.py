import socket

UDP_IP = "127.0.0.1"  # O mesmo IP que está ouvindo
UDP_PORT = 10001
MESSAGE = b"Hello, World!"  # Mensagem a ser enviada

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
print("Mensagem enviada!")
