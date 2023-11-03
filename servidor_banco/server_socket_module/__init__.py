import socket
from multiprocessing import Process, Lock, Array

class ServerSocket():
    def __init__(self, ip: int, porta: int):
        self.s = socket.create_server((ip,porta), family=socket.AF_INET)
        # PARA ADICIONAR COMANDOS A GENTE PODE ADICIONAR O COMANDO AQUI NESSE DICIONÁRIO E DEPOIS DEFINIR NA PROPRIA CLASSE O MÉTODO QUE VAMOS CHAMAR
        self.commands = {
                'add': self.add_cmd,
                'sub': self.sub_cmd
                }

    def start_server():
        bankLock = Lock()
        serverAccounts = Array(lock=bankLock)
        while True:
            c, addr = self.s.accept()
            fmsg = c.recv(1)
            for key in self.commands.keys():
                if (fmsg==key):
                    p = Process(target=self.commands[key], args=serverAccounts)
                    p.start()
        pass
