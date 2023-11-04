import socket

class ClientSocket():
    _balancecmd = "0".encode("ascii")
    _depositcmd = "1".encode("ascii")
    _withdrawcmd = "2".encode("ascii")
    _transfercmd = "3".encode("ascii")
    
    def __init__(self, ip, port) -> None: 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,port)
    
    def connect(self):
        self.s.connect(self.addr)
    
    def shtdnw_close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def balance(self, account):
        print("Saldo da conta {}".format(account))
        self.s.send(self._balancecmd)
        
    def deposit(self, account, value):
        print("Deposito de {:.2f} na conta {}".format(value, account))
        self.s.send(self._depositcmd)
        
    def withdraw(self, account, value):
        print("Saque de {:.2f} na conta {}".format(value, account))
        self.s.send(self._withdrawcmd)
    
    def transfer(self, src_account, dst_account, value):
        print("Transferencia de {:.2f} da conta {} para a conta {}".format(value, src_account, dst_account))
        self.s.send(self.transfer)
    

        