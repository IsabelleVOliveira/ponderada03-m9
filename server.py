import socket
import struct

# Cria um socket RAW que escuta pacotes diretamente da interface de rede (nível Ethernet)
interface_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

print("Aguardando pacotes UDP na porta 1100...")

# loop p/ escutar pacotes
while True:
    # Recebe o pacote 
    pacote, endereco = interface_socket.recvfrom(65536)

    # Cabeçalho Ethernet (14 bytes)
    tamanho_ethernet = 14
    # Extrai o cabeçalho IP
    cabeçalho_ip = pacote[tamanho_ethernet:tamanho_ethernet + 20]
    # Desempacota o cabeçalho IP nos campos definidos
    ip_fields = struct.unpack('!BBHHHBBH4s4s', cabeçalho_ip)
    # Campo que indica o protocolo (1=ICMP, 6=TCP, 17=UDP)
    protocolo = ip_fields[6]
    if protocolo != socket.IPPROTO_UDP:
        continue  # Ignora se não for UDP

    # Define onde começa o cabeçalho
    inicio_udp = tamanho_ethernet + 20
    # extrai os bytes
    cabecalho_udp = pacote[inicio_udp:inicio_udp + 8]
    # desempacota o cabeçalho UDP 
    campos_udp = struct.unpack('!HHHH', cabecalho_udp)

    porta_origem, porta_destino = campos_udp[0], campos_udp[1]

    # Filtro para porta de destino 1100
    if porta_destino == 1100:
        # Extrai os dados (payload) do pacote UDP
        mensagem = pacote[inicio_udp + 8:]
        try:
            conteudo = mensagem.decode(errors='ignore')
        except UnicodeDecodeError:
            conteudo = "<dados não decodificáveis>"

        print(f"Recebido de {porta_origem} para {porta_destino}: {conteudo}")
