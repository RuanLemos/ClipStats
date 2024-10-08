import socket

# Configurações do socket
HOSTRecv = "0.0.0.0"  # Ouvir em todas as interfaces
PORTRecv = 10001
BUFFER_SIZE = 2048

# Criação do socket UDP
ETHRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ETHRecv.bind((HOSTRecv, PORTRecv))
ETHRecv.settimeout(2.5)  # Tempo limite de 2.5 segundos

print("Aguardando dados na porta", PORTRecv)

def recvETH():
    try:
        print(BUFFER_SIZE)
        print(ETHRecv)
        data, addr = ETHRecv.recvfrom(BUFFER_SIZE)
        print('Dados recebidos:', data.decode(errors='ignore'))
        return data.decode(errors='ignore')
    except socket.timeout:
        return 'AA'
    except Exception as e:
        print(f'Erro ao receber dados: {e}')
        return None

# Loop de recepção
while True:
    recvETH()
