from .commHandler import commHandler

class SingletonConsoleModule():
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getLoop(self,socketModule,clock):
        x = input("> ")
        comando = x.split()
        comando = commHandler(comando, socketModule, clock)
        saida = comando.exec()
        print("[Console Output] ", saida[0], "Clock: ", saida[1])
        return saida[1]






