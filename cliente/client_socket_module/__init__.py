import socket
import struct

# Classe principal do cliente
class ClientSocket():
    # Comandos que podem ser enviados pelo cliente, em bytes
    _balancecmd = b'\x01'
    _depositcmd = b'\x02'
    _withdrawcmd = b'\x03'
    _transfercmd = b'\x04'
    
    # Ajuste do clock lógico, de acordo com o algoritmo de Lamport
    def adjust_clock(self, clock_prog, clock_remt):
        return 1 + max(clock_prog,clock_remt)

    # Função auxiliar para enviar bytes
    def bytes_and_send(self, valor, string):
        valor = struct.pack(string, valor)
        self.s.send(valor)
    
    def __init__(self, ip, port) -> None: 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,int(port))

    def connect(self):
        self.s.connect(self.addr)
    
    def shtdnw_close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    # Operação de consulta de saldo de uma conta.
    # Recebe como parâmetros o RG da conta e o clock local
    def balance(self, account, clock):
        try:
            print("chega aq")

            # Envia o comando de consulta de saldo
            self.s.send(self._balancecmd)

            # Empacota e envia o RG e o clock local em bytes
            self.bytes_and_send(int(account), '!I')
            self.bytes_and_send(clock, '!I')

            # Recebe e desempacota o valor da conta e o clock remoto em bytes
            valor_float = self.s.recv(4)
            valor_float = struct.unpack('!f', valor_float)[0]
            clock_int = self.s.recv(4)
            clock_remt = struct.unpack('!I', clock_int)[0]

            # Ajusta o clock local
            clock = self.adjust_clock(clock, clock_remt)
            return (valor_float,clock)
        except Exception as e:
            print("chega aq erro")
            return (-1, clock-1)

    # Operação de depósito em uma conta.
    # Recebe como parâmetros o RG da conta, o valor a ser depositado e o clock local
    def deposit(self, account, value, clock):
        try:
            # Envia o comando de depósito
            self.s.send(self._depositcmd)

            # Empacota e envia o RG, o valor a ser depositado e o clock local em bytes
            self.bytes_and_send(int(account), '!I')
            self.bytes_and_send(float(value), '!f')
            self.bytes_and_send(int(clock), '!I')

            # Recebe e desempacota o clock remoto em bytes
            clock_int = self.s.recv(4)
            clock_remt = struct.unpack('!I', clock_int)[0]

            # Ajusta o clock local
            clock = self.adjust_clock(clock, clock_remt)
            return (1,clock)
        except Exception as e:
            print("Houve erro: ",e)

    # Operação de saque em uma conta.
    # Recebe como parâmetros o RG da conta, o valor a ser sacado e o clock local
    def withdraw(self, account, value, clock):
        # Envia o comando de saque
        self.s.send(self._withdrawcmd)
        try:
            # Empacota e envia o RG, o valor a ser sacado e o clock local em bytes
            self.bytes_and_send(int(account), '!I')
            self.bytes_and_send(float(value), '!f')
            self.bytes_and_send(int(clock), '!I')

            # Recebe e desempacota o valor da conta e o clock remoto em bytes
            valor_bytes = self.s.recv(4)
            clock_int = self.s.recv(4)
            valor_total = struct.unpack('!f', valor_bytes)[0]
            clock_remt = struct.unpack('!I', clock_int)[0]

            # Ajusta o clock local
            clock = self.adjust_clock(clock, clock_remt)
            return (valor_total,clock)
        except Exception as e:
            print("Houve erro: ",e)
    
    # Operação de transferência entre contas.
    # Recebe como parâmetros o RG da conta de origem, o RG da conta de destino, o valor a ser transferido e o clock local
    def transfer(self, src_account, dst_account, value, clock):
        # Envia o comando de transferência
        self.s.send(self._transfercmd)
        try:
            # Empacota e envia o RG da conta de origem, o valor a ser transferido, o RG da conta de destino e o clock local em bytes
            self.bytes_and_send(int(src_account), '!I')
            self.bytes_and_send(float(value), '!f')
            self.bytes_and_send(int(dst_account), '!I')
            self.bytes_and_send(int(clock), '!I')

            # Recebe e desempacota o valor transferido e o clock remoto em bytes
            valor_bytes = self.s.recv(4)
            clock_int = self.s.recv(4)
            valor_total = struct.unpack('!f', valor_bytes)[0]
            clock_remt = struct.unpack('!I', clock_int)[0]

            # Ajusta o clock local
            clock = self.adjust_clock(clock, clock_remt)
            return (valor_total,clock)
        except Exception as e:
            print("Houve erro: ",e)
    

        
