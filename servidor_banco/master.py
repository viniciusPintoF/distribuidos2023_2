import argparse
from server_socket_module import ServerSocket
try:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--ip", help="Ip da interface em que deve escutar", default="localhost")
    parser.add_argument("--porta", help="Porta em que deve escutar", default=9999)
except Exception as err:
    print("Erro lendo argumentos: ", err)
    
try: 
    args = parser.parse_args()
    s = ServerSocket(ip=args.ip, porta=int(args.porta))
    s.start_server()
except Exception as err:
    print("Erro inicializando servidor: ", err)
