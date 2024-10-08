import socket

server = ("","")
Recv_TPU = ("","")

environment = socket.gethostname()
print(environment)
if (environment == 'KRAMM148' or environment == 'fedora' or environment == 'localhost.localdomain' or environment == 'RickP'):
	HOSTSend = "127.0.0.1"
	print('Rodando Local')
else:
	HOSTSend = "192.168.2.1"
	print('Rodando no Robo')

print(HOSTSend)
TCP_PORT = 10000
BUFFER_SIZE = 2048
server_address = ((HOSTSend, TCP_PORT))
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Porta de recebimento de dados CPU Controle Motores
HOSTRecv = ""
PORTRecv = 10001
OrigRecv = (HOSTRecv, PORTRecv)

# Porta de Recebimento de posicao da CPU Controle Motores
PORTRecvPosit = 10002
PosRecv = (HOSTRecv, PORTRecvPosit)

ETHRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


ETHPosRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Pra tentar conectar em no máximo 2.5 segundos
ETHRecv.settimeout(2.5)

def init():
	ETHRecv.bind(OrigRecv)
	ETHPosRecv.bind(PosRecv)

def send(string):
	ser.sendto(str.encode(string), server_address)

def recvSer():
	global server
	print(BUFFER_SIZE)
	print(server)
	data, server = ser.recvfrom(BUFFER_SIZE)
	return data.decode(errors='ignore')

def recvETH():
	global server
	try:
		data, server = ETHRecv.recvfrom(BUFFER_SIZE)
		print('data in recvETH(): ', data.decode(errors='ignore'))
		return data.decode(errors='ignore')
	except socket.timeout:
		print("Timeout: Couldn't connect in time")
		return 'AA'

def recvETHPos():
	global Recv_TPU
	data, Recv_TPU = ETHPosRecv.recvfrom(BUFFER_SIZE)
	return data.decode(errors='ignore')

def close():
	ser.close()
	ETHRecv.close()
	ETHPosRecv.close()
