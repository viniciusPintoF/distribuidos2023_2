from .client_socket_module import ClientSocket

class CommHandler():
    _instance = None
    def __init__(self, socketHandler, comando, clock):
        self.socketHandler = socketHandler
        self.comando = comando
        self.clock = clock 
        return cls._instance

    def exec(self):
        try:
            if self.comand[0] == "balanco":
                saida = self.socketHandler.balance(self.comando[1])
            elif self.comando[0] == "deposito":
                saida = self.socketHandler.deposit(self.comando[1], self.comando[2])
            elif self.comando[0] == "saque":
                saida = self.socketHandler.withdraw(self.comando[1], self.comando[2])
            elif self.comando[0] == "transferencia":
                saida = self.socketHandler.transfer(self.comando[1], self.comando[2], self.comando[3])
            else:
                saida = ("Erro de seleção", self.clock)
            return saida






