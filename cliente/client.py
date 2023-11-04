import argparse
from client_socket_module import ClientSocket

# Lida com argumentos
CMD_SALDO = 'saldo'
CMD_SAQUE = 'saque'
CMD_DEPOSITO = 'deposito'
CMD_TRANSFERENCIA = 'transf'
help_commands = """operação a ser realizada
    saldo: exibe o saldo da conta
    saque: realiza um saque na conta
    deposito: realiza um deposito na conta
    transf: transfere valor da conta acessada para a conta DESTINO
"""
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("conta", type=str, help="rg associado a conta acessada")
parser.add_argument("operacao", choices=[CMD_SALDO, CMD_SAQUE, CMD_DEPOSITO, CMD_TRANSFERENCIA], help=help_commands)
parser.add_argument("-v", "--valor", type=float, help="valor monetario da operacao")
parser.add_argument("-d", "--destino", help="rg associado a conta destino da transferencia")
args = parser.parse_args()
print(args)
# exit(0)

# Estabelece conexão com o servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 65432
try:
    print("Estabelecendo conexão com o servidor...")
    s = ClientSocket(SERVER_IP, SERVER_PORT)
    s.connect()
except Exception as e:
    print("Erro conectando ao servidor:")
    print(e)
    exit(1)
else:
    print("Conexão estabelecida.")

# Realiza operação
if args.operacao == CMD_SALDO:
    s.balance(args.conta)
if args.operacao == CMD_DEPOSITO:
    if not args.valor:
        print("sem valor de deposito, digite python3 client.py -h para ajuda.")
        exit(1)
    s.deposit(args.conta, args.valor)
if args.operacao == CMD_SAQUE:
    if not args.valor:
        print("sem valor de saque, digite python3 client.py -h para ajuda.")
        exit(1)
    s.withdraw(args.conta, args.valor)
if args.operacao == CMD_TRANSFERENCIA:
    if not args.valor:
        print("sem valor de transferencia, digite python3 client.py -h para ajuda.")
        exit(1)
    if not args.destino:
        print("sem destino de transferencia, digite python3 client.py -h para ajuda.")
        exit(1)
    s.transfer(args.conta, args.destino, args.valor)
    
    