from client_socket_module import ClientSocket

class CommHandler():
    _instance = None
    def __init__(self, cs, comando, clock):
        self.cs = cs 
        self.comando = comando
        self.clock = clock 

    def exec(self):
        try:
            if self.comando[0] == "balanco":
                saida = self.cs.balance(self.comando[1], clock=self.clock)
                saida = (f"O saldo atual é: {saida[0]}", saida[1])
            elif self.comando[0] == "deposito":
                saida = self.cs.deposit(self.comando[1], self.comando[2], clock=self.clock)
                saida = (f"O valor foi depositado com sucesso", saida[1])
            elif self.comando[0] == "saque":
                saida = self.cs.withdraw(self.comando[1], self.comando[2], clock=self.clock)
                saida = (f"O valor restante na conta é de: {saida[0]}", saida[1])
            elif self.comando[0] == "transferencia":
                saida = self.cs.transfer(self.comando[1], self.comando[3], self.comando[2], clock=self.clock)
                saida = (f"O valor transferido foi: {saida[0]}", saida[1])
            else:
                saida = ("Erro de seleção", self.clock-1)
        except Exception as e:
            saida = (f"Erro com bloco: \n\n{e}", self.clock-1)
        return saida
