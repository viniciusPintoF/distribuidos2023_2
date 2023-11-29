import socket
from multiprocessing import Process, Manager
import struct 

# Classe principal do servidor
class ServerSocket():
    def __init__(self, ip: int, porta: int):
        self.ip = ip
        self.porta = porta

        # Cria um socket de servidor
        self.s = socket.create_server((ip,porta), family=socket.AF_INET)

        # Dicionario de transações a serem executadas pelo servidor
        self.commands = {
                b'\x01' : self.balanco,
                b'\x02' : self.deposito,
                b'\x03' : self.saque,
                b'\x04' : self.transferencia 
                }

    # Ajuste do clock lógico, de acordo com o algoritmo de Lamport
    # Recebe como parâmetros o clock local e o clock remoto. Retorna o clock atualizado
    def adjust_clock(self, clock_prog, clock_remt):
        return 1 + max(clock_prog,clock_remt)

    # Operação de consulta de saldo de uma conta.
    # Recebe como parâmetros o socket de conexão do cliente, o dicionário de contas e o clock local
    def balanco(self,c,proxy_dict,clock_l):
        # Incrementa o clock local
        clock_local = clock_l.value
        clock_local += 1
        print("Balanco procurado:", proxy_dict)

        # Recebe o RG do cliente e o clock remoto em bytes
        rg_bytes = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            # Trata os bytes recebidos
            rg_int = struct.unpack('!I', rg_bytes)[0]
            clock_remt = struct.unpack('!I', clock_bytes)[0]

            # Atualizando o clock a ser registrado pelo servidor e o cliente
            clock = self.adjust_clock(clock_local, clock_remt)

            # Se o RG não estiver no dicionário, adiciona-o com valor 0
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0
            valor_conta = proxy_dict[rg_int]

            # Empacota o valor da conta e o clock local em bytes
            bytes_data = struct.pack('!f',valor_conta)
            clock_bytes = struct.pack('!I',clock_local)
            print("Enviando arquivos...")

            # Envia os bytes para o cliente
            c.send(bytes_data)
            c.send(clock_bytes)

            # Atualiza o clock local
            clock_l.value = clock
        except Exception as e:
            print("Erro no balanco", e)
            exit(1)

    # Operação de depósito em uma conta.
    # Recebe como parâmetros o socket de conexão do cliente, o dicionário de contas e o clock local
    def deposito(self,c,proxy_dict,clock_l):
        # Incrementa o clock local
        clock_local = clock_l.value
        clock_local += 1
        print("Deposito :", proxy_dict)

        # Recebe o RG do cliente, o valor a ser depositado e o clock remoto em bytes
        rg_bytes = c.recv(4)
        valor_bytes = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            # Trata os bytes recebidos
            rg_int = struct.unpack('!I', rg_bytes)[0]
            valor_float = round(struct.unpack('!f', valor_bytes)[0],2)
            clock_remt = struct.unpack('!I', clock_bytes)[0]

            # Atualizando o clock a ser registrado pelo servidor e o cliente
            clock = self.adjust_clock(clock_local, clock_remt)

            # Se o RG não estiver no dicionário, adiciona-o com valor 0
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0.0

            # Atualiza o valor da conta
            proxy_dict[rg_int] += valor_float

            # Empacota o clock local em bytes
            clock_bytes = struct.pack('!I',clock_local)
            print("Enviando arquivos...")

            # Envia os bytes para o cliente
            c.send(clock_bytes)

            # Atualiza o clock local
            clock_l.value = clock
        except Exception as e:
            print("Erro no balanco", e)
            exit(1)

    # Operação de saque em uma conta.
    # Recebe como parâmetros o socket de conexão do cliente, o dicionário de contas e o clock local
    def saque(self,c,proxy_dict,clock_l):
        # Incrementa o clock local
        clock_local = clock_l.value
        clock_local += 1
        print("Saque :", proxy_dict)

        # Recebe o RG do cliente, o valor a ser sacado e o clock remoto em bytes
        rg_bytes = c.recv(4)
        valor_bytes = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            # Trata os bytes recebidos
            rg_int = struct.unpack('!I', rg_bytes)[0]
            valor_float = round(struct.unpack('!f', valor_bytes)[0],2)
            clock_remt = struct.unpack('!I', clock_bytes)[0]

            # Atualizando o clock a ser registrado pelo servidor e o cliente
            clock = self.adjust_clock(clock_local, clock_remt)

            # Se o RG não estiver no dicionário, adiciona-o com valor 0
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0.0

            # Atualiza o valor da conta caso haja saldo suficiente
            if proxy_dict[rg_int]  >= valor_float:
                proxy_dict[rg_int] -= valor_float
                valor_total = proxy_dict[rg_int]
            
            # Caso contrário, o balanço é zerado
            else:
                valor_total = 0
                proxy_dict[rg_int] = 0

            # Empacota o valor da conta e o clock local em bytes
            valor_bytes = struct.pack('!f',valor_total)
            clock_bytes = struct.pack('!I',clock_local)
            print("Enviando arquivos...")

            # Envia os bytes para o cliente
            c.send(valor_bytes)
            c.send(clock_bytes)

            # Atualiza o clock local
            clock_l.value = clock
        except Exception as e:
            print("Erro no balanco", e)
            exit(1)

    # Operação de transferência entre contas.
    # Recebe como parâmetros o socket de conexão do cliente, o dicionário de contas e o clock local
    def transferencia(self,c,proxy_dict,clock_l):
        # Incrementa o clock local
        clock_local = clock_l.value
        clock_local += 1
        print("Transferencia :", proxy_dict)

        # Recebe o RG do cliente, o valor a ser transferido, o RG do destinatário e o clock remoto em bytes
        rg_bytes = c.recv(4)
        valor_bytes = c.recv(4)
        rg_bytes2 = c.recv(4)
        clock_bytes = c.recv(4)
        try:
            # Trata os bytes recebidos
            rg_int = struct.unpack('!I', rg_bytes)[0]
            valor_float = round(struct.unpack('!f', valor_bytes)[0],2)
            rg_int2 = struct.unpack('!I', rg_bytes2)[0]
            clock_remt = struct.unpack('!I', clock_bytes)[0]

            # Atualizando o clock a ser registrado pelo servidor e o cliente
            clock = self.adjust_clock(clock_local, clock_remt)

            # Se o RG do remetente não estiver no dicionário, adiciona-o com valor 0
            if not rg_int in proxy_dict:
                proxy_dict[rg_int] = 0.0
            
            # Atualiza o valor da conta caso haja saldo suficiente na conta de origem
            if proxy_dict[rg_int]  >= valor_float:
                proxy_dict[rg_int] = proxy_dict[rg_int] - valor_float

            # Caso contrário, todo o valor da conta de origem é transferido
            else:
                valor_float = proxy_dict[rg_int] 
                proxy_dict[rg_int] = 0

            # Se o RG do destinatário não estiver no dicionário, adiciona-o com valor 0
            if not rg_int2 in proxy_dict:
                proxy_dict[rg_int2] = 0.0

            # Atualiza o valor da conta de destino
            proxy_dict[rg_int2] = proxy_dict[rg_int2] + valor_float

            # Empacota o valor da conta e o clock local em bytes
            valor_bytes = struct.pack('!f',valor_float)
            clock_bytes = struct.pack('!I',clock_local)
            print(f"{proxy_dict}")

            # Envia os bytes para o cliente
            c.send(valor_bytes)
            c.send(clock_bytes)

            # Atualiza o clock local
            clock_l.value = clock
        except Exception as e:
            print("Erro na transferecia", e)
            exit(1)

    # Função que trata a conexão de um cliente
    def connectionHandler(self,c,proxy_dict,clock):
        # Loop que fica escutando por mensagens do cliente
        while True:
            print(f"Estado das contas: {proxy_dict}   Clock interno: {clock}")
            fmsg = c.recv(1)
            # Se a mensagem for vazia, sai do loop
            if not fmsg:
                break
            # Se a mensagem for uma das operações, executa-a
            for key in self.commands.keys():
                if (fmsg==key):
                    self.commands[key](c,proxy_dict,clock)

    # Função que inicializa o servidor
    def start_server(self):
        with Manager() as manager:
            proxy_dict = manager.dict()
            clock_l = manager.Value('I',0)
            while True:
                print("Servidor up e escutando em:", self.ip, self.porta)
                c, addr = self.s.accept()
                p = Process(target=self.connectionHandler, args=[c,proxy_dict,clock_l])
                p.start()

