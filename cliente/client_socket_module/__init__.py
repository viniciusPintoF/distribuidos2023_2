import socket
import struct

# Classe principal do cliente
class ClientSocket():
    # Comandos das transações
    _balancecmd = b'\x01'
    _depositcmd = b'\x02'
    _withdrawcmd = b'\x03'
    _transfercmd = b'\x04'
    
    # Inicializa o socket do cliente
    def __init__(self, ip, port) -> None: 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,int(port))
        self.lamport_clock = 0
    
    def connect_and_loop(self):
        self.s.connect(self.addr)
    
    def shtdnw_close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    # Operação de consulta de saldo de uma conta. Recebe como parâmetro o RG da conta
    def balance(self, account):
        try:
            # Envio do comando de consulta de saldo ao servidor
            self.s.send(self._balancecmd)
            print("Saldo da conta {}:".format(account))

            # Empacota o RG da conta em bytes e envia ao servidor
            bytes_account = struct.pack('!I', int(account))

            # Envio do RG da conta ao servidor
            self.s.send(bytes_account)

            # Recebe o valor da conta e o clock do servidor
            valor_conta = self.s.recv(8)

            # Trata os bytes recebidos
            valor_float = struct.unpack('!f', valor_conta[0:4])[0]
            clock = struct.unpack('!I', valor_conta[4:8])[0]

            # Retorna o valor da conta e o clock
            return valor_float,clock
        except Exception as e:
            print("Houve erro: ",e)


    # Operação de depósito em uma conta. Recebe como parâmetros o RG da conta e o valor a ser depositado
    def deposit(self, account, value):
        try:
            print("Deposito de {:.2f} na conta {}".format(value, account))
            # Envio do comando de depósito ao servidor
            self.s.send(self._depositcmd)

            # Empacota o RG da conta e o valor a ser depositado em bytes
            bytes_account = struct.pack('!I', int(account))
            bytes_value = struct.pack('!f', round(value,2))

            # Envio do RG da conta e o valor a ser depositado ao servidor
            self.s.send(bytes_account)
            self.s.send(bytes_value)
        except Exception as e:
            print("Houve erro: ",e)

    # Operação de saque de uma conta. Recebe como parâmetros o RG da conta e o valor a ser sacado        
    def withdraw(self, account, value):
        print("Saque de {:.2f} na conta {}".format(value, account))
        # Envio do comando de saque ao servidor
        self.s.send(self._withdrawcmd)
    
    # Operação de transferência entre contas. Recebe como parâmetros o RG da conta de origem, o RG da conta de destino e o valor a ser transferido
    def transfer(self, src_account, dst_account, value):
        print("Transferencia de {:.2f} da conta {} para a conta {}".format(value, src_account, dst_account))
        self.s.send(self.transfer)
    

        
