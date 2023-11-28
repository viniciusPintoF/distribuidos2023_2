import socket
import json

HEADER_SIZE = 64
FORMAT = 'ascii'
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
    

class ClientSocket():
    _balancecmd = '0'
    _depositcmd = '1'
    _withdrawcmd = '2'
    _transfercmd = '3'
    
    def __init__(self, ip, port) -> None: 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,port)
    
    def connect(self):
        self.s.connect(self.addr)
    
    def shtdnw_close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def balance(self, account):
        print(f"Saldo da conta com RG {account}:")
        # Sending command
        self.s.send(self._balancecmd.encode(FORMAT))
        # Sending data
        data = {'rg':account}
        send_json(self.s, data)
        # Receiving response
        response = receive_json(self.s)
        balance_value = response['balance']
        print("R$ {:.2f}".format(balance_value))
        
    def deposit(self, account, value):
        print("Deposito de {:.2f} na conta {}".format(value, account))
        # Sending command
        self.s.send(self._depositcmd.encode(FORMAT))
        # Sending data
        data = {'rg':account, 'value': value}
        send_json(self.s, data)
        # Receiving response
        response = receive_json(self.s)
        balance_value = response['balance']
        print("Novo saldo: R$ {:.2f}".format(balance_value))
        
        
    def withdraw(self, account, value):
        print("Saque de {:.2f} na conta {}".format(value, account))
        # Sending command
        self.s.send(self._withdrawcmd.encode(FORMAT))
        # Sending data
        data = {'rg':account, 'value': value}
        send_json(self.s, data)
        # Receiving response
        response = receive_json(self.s)
        balance_value = response['balance']
        print("Novo saldo: R$ {:.2f}".format(balance_value))
    
    def transfer(self, src_account, dst_account, value):
        print("Transferência de {:.2f} da conta {} para a conta {}".format(value, src_account, dst_account))
        # Sending command
        self.s.send(self._transfercmd.encode(FORMAT))
        # Sending data
        data = {'rg':src_account, 'value': value, 'destination': dst_account}
        send_json(self.s, data)
        # Receiving response
        response = receive_json(self.s)
        balance_value = response['balance']
        print("Novo saldo: R$ {:.2f}".format(balance_value))
    

        