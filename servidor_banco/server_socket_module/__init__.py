import socket
from multiprocessing import Process, Manager
import struct 
class ServerSocket():
    def __init__(self, ip: int, porta: int):
        self.ip = ip
        self.porta = porta
        self.s = socket.create_server((ip,porta), family=socket.AF_INET)
        # PARA ADICIONAR COMANDOS A GENTE PODE ADICIONAR O COMANDO AQUI NESSE DICIONÁRIO E DEPOIS DEFINIR NA PROPRIA CLASSE O MÉTODO QUE VAMOS CHAMAR
        self.commands = {
                b'\x01' : self.balanco,
                b'\x02' : self.deposito,
                b'\x03' : self.saque,
                b'\x04' : self.transferencia 
                }

    def adjust_clock(self, clock_prog, clock_remt):
        return 1 + max(clock_prog,clock_remt)

    def balanco(self,c,proxy_dict,clock_l):
        clock_local = clock_l.value
        clock_local += 1
        print("Balanco procurado:", proxy_dict)
        rg_bytes = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            rg_int = struct.unpack('!I', rg_bytes)[0]
            clock_remt = struct.unpack('!I', clock_bytes)[0]
            clock = self.adjust_clock(clock_local, clock_remt)
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0
            valor_conta = proxy_dict[rg_int]
            bytes_data = struct.pack('!f',valor_conta)
            clock_bytes = struct.pack('!I',clock_local)
            print("Enviando arquivos...")
            c.send(bytes_data)
            c.send(clock_bytes)
            clock_l.value = clock
        except Exception as e:
            print("Erro no balanco", e)
            exit(1)

    def deposito(self,c,proxy_dict,clock_l):
        clock_local = clock_l.value
        clock_local += 1
        print("Deposito :", proxy_dict)
        rg_bytes = c.recv(4)
        valor_bytes = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            rg_int = struct.unpack('!I', rg_bytes)[0]
            valor_float = round(struct.unpack('!f', valor_bytes)[0],2)
            clock_remt = struct.unpack('!I', clock_bytes)[0]
            clock = self.adjust_clock(clock_local, clock_remt)
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0.0
            proxy_dict[rg_int] += valor_float
            clock_bytes = struct.pack('!I',clock_local)
            print("Enviando arquivos...")
            c.send(clock_bytes)
            clock_l.value = clock
        except Exception as e:
            print("Erro no balanco", e)
            exit(1)

    def saque(self,c,proxy_dict,clock_l):
        clock_local = clock_l.value
        clock_local += 1
        print("Saque :", proxy_dict)
        rg_bytes = c.recv(4)
        valor_bytes = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            rg_int = struct.unpack('!I', rg_bytes)[0]
            valor_float = round(struct.unpack('!f', valor_bytes)[0],2)
            clock_remt = struct.unpack('!I', clock_bytes)[0]
            clock = self.adjust_clock(clock_local, clock_remt)
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0.0
            if proxy_dict[rg_int]  >= valor_float:
                proxy_dict[rg_int] -= valor_float
                valor_total = proxy_dict[rg_int]
            else:
                valor_total = 0
                proxy_dict[rg_int] = 0
            valor_bytes = struct.pack('!f',valor_total)
            clock_bytes = struct.pack('!I',clock_local)
            print("Enviando arquivos...")
            c.send(valor_bytes)
            c.send(clock_bytes)
            clock_l.value = clock
        except Exception as e:
            print("Erro no balanco", e)
            exit(1)

    def transferencia(self,c,proxy_dict,clock_l):
        clock_local = clock_l.value
        clock_local += 1
        print("Transferencia :", proxy_dict)
        rg_bytes = c.recv(4)
        valor_bytes = c.recv(4)
        rg_bytes2 = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            rg_int = struct.unpack('!I', rg_bytes)[0]
            valor_float = round(struct.unpack('!f', valor_bytes)[0],2)
            rg_int2 = struct.unpack('!I', rg_bytes2)[0]
            clock_remt = struct.unpack('!I', clock_bytes)[0]
            clock = self.adjust_clock(clock_local, clock_remt)
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0.0
            if proxy_dict[rg_int]  >= valor_float:
                proxy_dict[rg_int] = proxy_dict[rg_int] - valor_float
            else:
                valor_float = proxy_dict[rg_int] 
                proxy_dict[rg_int] = 0

            if not rg_int2 in proxy_dict:
                proxy_dict[rg_int2] = 0.0
            proxy_dict[rg_int2] = proxy_dict[rg_int2] + valor_float
            valor_bytes = struct.pack('!f',valor_float)
            clock_bytes = struct.pack('!I',clock_local)
            print(f"{proxy_dict}")
            c.send(valor_bytes)
            c.send(clock_bytes)
            clock_l.value = clock
        except Exception as e:
            print("Erro na transferecia", e)
            exit(1)

    def connectionHandler(self,c,proxy_dict,clock):
        while True:
            print(f"Estado das contas: {proxy_dict}   Clock interno: {clock}")
            fmsg = c.recv(1)
            if not fmsg:
                break
            for key in self.commands.keys():
                if (fmsg==key):
                    self.commands[key](c,proxy_dict,clock)

    def start_server(self):
        with Manager() as manager:
            proxy_dict = manager.dict()
            clock_l = manager.Value('I',0)
            while True:
                print("Servidor up e escutando em:", self.ip, self.porta)
                c, addr = self.s.accept()
                p = Process(target=self.connectionHandler, args=[c,proxy_dict,clock_l])
                p.start()

