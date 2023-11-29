import socket
import struct

class ClientSocket():
    _balancecmd = b'\x01'
    _depositcmd = b'\x02'
    _withdrawcmd = b'\x03'
    _transfercmd = b'\x04'
    
    def adjust_clock(self, clock_prog, clock_remt):
        return 1 + max(clock_prog,clock_remt)

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

    def balance(self, account, clock):
        try:
            print("chega aq")
            self.s.send(self._balancecmd)
            self.bytes_and_send(int(account), '!I')
            self.bytes_and_send(clock, '!I')
            valor_float = self.s.recv(4)
            valor_float = struct.unpack('!f', valor_float)[0]
            clock_int = self.s.recv(4)
            clock_remt = struct.unpack('!I', clock_int)[0]
            clock = self.adjust_clock(clock, clock_remt)
            return (valor_float,clock)
        except Exception as e:
            print("chega aq erro")
            return (-1, clock-1)


    def deposit(self, account, value, clock):
        try:
            self.s.send(self._depositcmd)
            self.bytes_and_send(int(account), '!I')
            self.bytes_and_send(float(value), '!f')
            self.bytes_and_send(int(clock), '!I')
            clock_int = self.s.recv(4)
            clock_remt = struct.unpack('!I', clock_int)[0]
            clock = self.adjust_clock(clock, clock_remt)
            return (1,clock)
        except Exception as e:
            print("Houve erro: ",e)

    def withdraw(self, account, value, clock):
        self.s.send(self._withdrawcmd)
        try:
            self.bytes_and_send(int(account), '!I')
            self.bytes_and_send(float(value), '!f')
            self.bytes_and_send(int(clock), '!I')
            valor_bytes = self.s.recv(4)
            clock_int = self.s.recv(4)
            valor_total = struct.unpack('!f', valor_bytes)[0]
            clock_remt = struct.unpack('!I', clock_int)[0]
            clock = self.adjust_clock(clock, clock_remt)
            return (valor_total,clock)
        except Exception as e:
            print("Houve erro: ",e)
    
    def transfer(self, src_account, dst_account, value, clock):
        self.s.send(self._transfercmd)
        try:
            self.bytes_and_send(int(src_account), '!I')
            self.bytes_and_send(float(value), '!f')
            self.bytes_and_send(int(dst_account), '!I')
            self.bytes_and_send(int(clock), '!I')
            valor_bytes = self.s.recv(4)
            clock_int = self.s.recv(4)
            valor_total = struct.unpack('!f', valor_bytes)[0]
            clock_remt = struct.unpack('!I', clock_int)[0]
            clock = self.adjust_clock(clock, clock_remt)
            return (valor_total,clock)
        except Exception as e:
            print("Houve erro: ",e)
    

        
