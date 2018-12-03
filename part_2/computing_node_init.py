import json
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

    # first connect to seed node and get ip list
    computing_node_list = []
    while True:
        client_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_out.connect_ex((args.seed_ip, args.seed_port_in))
        send_msg(client_out, '#INIT#')
        raw_data = recv_msg(client_out)
        client_out.close()
        print(raw_data)
        try:
            computing_node_list = json.loads(raw_data)
        except Exception as e:
            print('JSONDecodeError')
        else:
            if type(computing_node_list) is list:
                break

    # start mine
    # listen in case got new block msg
    # send to others if get a new block
    # 
    client_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_in.bind((args.self_ip, args.self_port_in))
    client_in.listen(10)

    while True:
        client_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_out.connect_ex((args.seed_ip, args.seed_port_in))
        client_out.sendall('hello! from client!')
        raw_data = client_out.recv(4096)
        print(raw_data)
        time.sleep(3)
        client_out.close()

    client_in.close()
