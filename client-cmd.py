import socket
import time

HEADER = 64
SERVER = "192.168.1.204"
PORT = 5050
FORMAT = 'utf-8'
DC_MSG = "!DC"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

if __name__ == "__main__":

    while True:
        # message = input("Enter message to send: ")
        id = input("Enter LED ID (-1 to quit): ")
        if id == '-1':
            send(DC_MSG)
            break
        
        r = input("Enter RED value: ")
        g = input("Enter GREEN value: ")
        b = input("Enter BLUE value: ")

        message = f"N{id} R{r} G{g} B{b}"
        send(message)
