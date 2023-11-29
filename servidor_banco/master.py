import argparse
from server_socket_module import ServerSocket

try:
    # Cria um parser para os argumentos
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--ip", help="Ip da interface em que deve escutar", default="localhost")
    parser.add_argument("--porta", help="Porta em que deve escutar", default=9999)
    args = parser.parse_args()

    # Instancializa um servidor e o inicializa
    s = ServerSocket(ip=args.ip, porta=int(args.porta))
    s.start_server()
except Exception as e:
    print("Houve erro")
    print(e)
