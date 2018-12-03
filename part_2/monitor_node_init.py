import json
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

    # server_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_out.close()

    # packet = open('data_backup/mh0_packet.txt', 'w')
    # packet.write("%s: %s\n" % (addr, data))
    # packet.flush()

    computing_node_list = []

    while True:
        connect, addr = server_in.accept()
        raw_data = recv_msg(connect)
        print('Addr: {}.\nData: {}.'.format(addr, raw_data))
        if raw_data == '#INIT#':
            if addr[0] not in computing_node_list:
                computing_node_list.append(addr[0])
            send_msg(connect, '#IPLIST#{}'.format(json.dumps(computing_node_list)))
        elif raw_data == 'break':
            return
        else:
            continue
        connect.close()

    server_in.close()
