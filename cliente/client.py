import argparse
from consoleModule import SingletonConsoleModule
from client_socket_module import ClientSocket

# Lida com argumentos
help_commands = """operação a ser realizada
    saldo: exibe o saldo da conta
    saque: realiza um saque na conta
    deposito: realiza um deposito na conta
    transf: transfere valor da conta acessada para a conta DESTINO
"""

# Cria um parser para os argumentos
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("ip", help="IP Servidor")
parser.add_argument("-p", "--porta", default="9999", help="Porta")
args = parser.parse_args()

# Estabelece conexão com o servidor
try:
    print("Estabelecendo conexão com o servidor...")
    cs = ClientSocket(args.ip, args.porta)
    cm = SingletonConsoleModule()
    clock = 0
    cs.connect()
    print("Conexão com o servidor")
    while True:
        clock = cm.getLoop(cs,clock+1)
    s.shtdnw_close()
except Exception as e:
    print("Erro conectando ao servidor:")
    print(e)
    exit(1)

