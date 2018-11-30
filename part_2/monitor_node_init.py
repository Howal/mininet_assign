import socket
import argparse
from socket_util import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='receive server help')

    parser.add_argument('--self-ip', help='ip', default='localhost', type=str)
    parser.add_argument('--self-port-in', help='port', default=20000, type=int)
    args = parser.parse_args()

    server_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_in.bind((args.self_ip, args.self_port_in))
    server_in.listen(10)

    server_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # packet = open('data_backup/mh0_packet.txt', 'w')
    computing_node_list = []

    while True:
        print('---start')
        connect, addr = server_in.accept()
        print('---accept')

        total_data = []
        data = recv_msg(connect)
        print('---recv')
        print('{} + {}'.format(data, addr))
        # packet.write("%s: %s\n" % (addr, data))
        # packet.flush()
        send_msg(connect, '{} + from server.'.format(addr))
        print('---send')
        connect.close()
        print('---close')
    server_in.close()
    server_out.close()
