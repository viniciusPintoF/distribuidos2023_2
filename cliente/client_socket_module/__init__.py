import socket
import struct

class ClientSocket():
    _balancecmd = b'\x01'
    _depositcmd = b'\x02'
    _withdrawcmd = b'\x03'
    _transfercmd = b'\x04'
    
    def __init__(self, ip, port) -> None: 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,int(port))
        self.lamport_clock = 0
    
    def connect_and_loop(self):
        self.s.connect(self.addr)
    
    def shtdnw_close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def balance(self, account):
        try:
            self.s.send(self._balancecmd)
            print("Saldo da conta {}:".format(account))
            bytes_account = struct.pack('!I', int(account))
            self.s.send(bytes_account)
            valor_conta = self.s.recv(8)
            valor_float = struct.unpack('!f', valor_conta[0:4])[0]
            clock = struct.unpack('!I', valor_conta[4:8])[0]
            return valor_float,clock
        except Exception as e:
            print("Houve erro: ",e)


    def deposit(self, account, value):
        try:
            print("Deposito de {:.2f} na conta {}".format(value, account))
            self.s.send(self._depositcmd)
            bytes_account = struct.pack('!I', int(account))
            bytes_value = struct.pack('!f', round(value,2))
            self.s.send(bytes_account)
            self.s.send(bytes_value)
        except Exception as e:
            print("Houve erro: ",e)


        
    def withdraw(self, account, value):
        print("Saque de {:.2f} na conta {}".format(value, account))
        self.s.send(self._withdrawcmd)
    
    def transfer(self, src_account, dst_account, value):
        print("Transferencia de {:.2f} da conta {} para a conta {}".format(value, src_account, dst_account))
        self.s.send(self.transfer)
    

        
