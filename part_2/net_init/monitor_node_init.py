import socket
import argparse

s.sendto(args.data, (args.ip, args.port))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='receive server help')

    parser.add_argument('--self-ip', help='ip', default='127.0.0.1', type=str)
    parser.add_argument('--self-port', help='port', default=12345, type=int)
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((args.self_ip, args.self_port))

    packet = open('data_backup/mh0_packet.txt', 'w')

    while True:
        data, addr = s.recvfrom(512)
        packet.write("%s: %s\n" % (addr, data))
        packet.flush()
        data
