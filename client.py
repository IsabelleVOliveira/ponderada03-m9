import socket
import struct

# Configurações
ip_origem = "127.0.0.1"
ip_destino = "127.0.0.1"
porta_origem = 40000
porta_destino = 1100
mensagem = b"Mensagem via UDP RAW!"

# Construção do cabeçalho IP
versao_ihl = 0x45             # Versão 4, IHL = 5 (sem opções)
tipo_servico = 0              # serviço padrão
total_length = 20 + 8 + len(mensagem)  # cabeçalho IP + UDP + dados
identificacao = 9999          # Número de identificação do datagrama
flags_fragment = 0            # Sem fragmentação
ttl = 64                      # Time to Live
protocolo = socket.IPPROTO_UDP  # Protocolo UDP
checksum_ip = 0 

# Constrói o cabeçalho IP (20 bytes)
ip_header = struct.pack(
    "!BBHHHBBH4s4s",
    versao_ihl,
    tipo_servico,
    total_length,
    identificacao,
    flags_fragment,
    ttl,
    protocolo,
    checksum_ip,
    socket.inet_aton(ip_origem),
    socket.inet_aton(ip_destino)
)

# Cabeçalho UDP
comprimento_udp = 8 + len(mensagem)
checksum_udp = 0 

# Constrói o cabeçalho UDP
udp_header = struct.pack(
    "!HHHH",
    porta_origem,
    porta_destino,
    comprimento_udp,
    checksum_udp
)

# Pacote final: IP + UDP + payload
datagrama = ip_header + udp_header + mensagem

# Criar socket RAW e enviar
envio_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
envio_socket.sendto(datagrama, (ip_destino, 0))

print("Datagrama UDP enviado via socket RAW.")
