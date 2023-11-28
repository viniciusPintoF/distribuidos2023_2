import socket
from multiprocessing import Process, Lock, Array
import threading
import json

FORMAT = 'ascii'
HEADER_SIZE = 64
RG_SIZE = 10
VALUE_SIZE = 8

def send_json(conn, data):
    msg = json.dumps(data)
    
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' ' * (HEADER_SIZE - len(msg_length))
    conn.send(msg_length)

    conn.send(msg.encode(FORMAT))

def receive_json(conn):
    header = conn.recv(HEADER_SIZE).decode(FORMAT)
    msg_length = int(header)
    
    msg = conn.recv(msg_length).decode(FORMAT)
    data = json.loads(msg)
    return data
    

class ServerSocket():
    def __init__(self, ip: int, porta: int):
        self.ip = ip
        self.port = porta
        self.s = socket.create_server((ip,porta), family=socket.AF_INET)
        # bankLock = Lock()
        # self.serverAccounts = Array(lock=bankLock)
        self.accounts = {
            '1234567890': {'balance': 500.00},
            '0987654321': {'balance': 1000.00}
        }
        
        self.commands = {
            '0': self.balance,
            '1': self.deposit,
            '2': self.withdraw,
            '3': self.transfer
        }

    def start_server(self):
        print(f'[GERAL] Servidor iniciado')
        while True:
            print(f'[GERAL] Ouvindo em {self.ip}:{self.port}')
            conn, addr = self.s.accept()
            print(f'[GERAL] Conexão com {addr}')
            thread = threading.Thread(target=self.handle_client, args=(conn,addr))
            thread.start()
            
            
    def handle_client(self, conn, addr):
        cmdkey = conn.recv(1).decode(FORMAT)
        print(f'[CLIENTE {addr}] Comando {cmdkey}')
        
        if cmdkey in self.commands.keys():
            self.commands[cmdkey](conn, addr)
        else:
            print(f'[CLIENTE {addr}] Comando não encontrado')
        
                    
    def balance(self, conn, addr):
        print(f'[CLIENTE {addr}] Executando "Saldo"')
        
        data = receive_json(conn)
        print(f'[CLIENTE {addr}] Dados recebidos: {data}')
        
        rg_value = data['rg']
        balance_value = self.accounts[rg_value]['balance']
        response_data = {'balance': balance_value}
        send_json(conn, response_data)
        print(f'[CLIENTE {addr}] Dados enviados: {response_data}')
        
        conn.close()
        print(f'[CLIENTE {addr}] Conexão encerrada')
    
    def deposit(self, conn, addr):
        print(f'[CLIENTE {addr}] Executando "Depósito"')
        
        data = receive_json(conn)
        print(f'[CLIENTE {addr}] Dados recebidos: {data}')
        
        rg_value = data['rg']
        deposit_value = data['value']
        self.accounts[rg_value]['balance'] += deposit_value
        new_balance = self.accounts[rg_value]['balance']
        response_data = {'balance': new_balance}
        send_json(conn, response_data)
        print(f'[CLIENTE {addr}] Dados enviados: {response_data}')
        
        conn.close()
        print(f'[CLIENTE {addr}] Conexão encerrada') 
        
    def withdraw(self, conn, addr):
        print(f'[CLIENTE {addr}] Executando "Saque"')
        
        data = receive_json(conn)
        print(f'[CLIENTE {addr}] Dados recebidos: {data}')
        
        rg_value = data['rg']
        withdraw_value = data['value']
        self.accounts[rg_value]['balance'] -= withdraw_value
        new_balance = self.accounts[rg_value]['balance']
        response_data = {'balance': new_balance}
        send_json(conn, response_data)
        print(f'[CLIENTE {addr}] Dados enviados: {response_data}')
        
        conn.close()  
        print(f'[CLIENTE {addr}] Conexão encerrada') 
        
    def transfer(self, conn, addr):
        print(f'[CLIENTE {addr}] Executando "Transaferência"')
        
        data = receive_json(conn)
        print(f'[CLIENTE {addr}] Dados recebidos: {data}')
        
        rg_value = data['rg']
        transfer_value = data['value']
        destination = data['destination']
        
        self.accounts[rg_value]['balance'] -= transfer_value
        self.accounts[destination]['balance'] += transfer_value
        
        new_balance = self.accounts[rg_value]['balance']
        response_data = {'balance': new_balance}
        send_json(conn, response_data)
        print(f'[CLIENTE {addr}] Dados enviados: {response_data}')
        
        conn.close()  
        print(f'[CLIENTE {addr}] Conexão encerrada')   


