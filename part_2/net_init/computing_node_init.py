import socket
import argparse
import time
from socket_util import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='receive server help')

    parser.add_argument('--self-ip', help='ip', default='localhost', type=str)
    parser.add_argument('--self-port-in', help='port', default=20000, type=int)
    parser.add_argument('--seed-ip', help='ip', default='10.0.0.99', type=str)
    parser.add_argument('--seed-port-in', help='port', default=20000, type=int)
    args = parser.parse_args()

    # first connect to seed node
    client_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_out.connect((args.seed_ip, args.seed_port_in))
    mystring = ''
    for i in range(10000):
        mystring = '{} init{}'.format(mystring, i)
    send_msg(client_out, mystring)
    data = recv_msg(client_out)
    print(data)
    time.sleep(3)
    client_out.close()

    #
    client_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_in.bind((args.self_ip, args.self_port_in))
    client_in.listen(10)

    while True:
        client_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_out.connect((args.seed_ip, args.seed_port_in))
        client_out.sendall('hello! from client!')
        data = client_out.recv(4096)
        print(data)
        time.sleep(3)
        client_out.close()

    client_in.close()
