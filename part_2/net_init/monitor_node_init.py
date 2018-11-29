import socket
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='receive server help')

    parser.add_argument('--self-ip', help='ip', default='localhost', type=str)
    parser.add_argument('--self-port', help='port', default=12345, type=int)
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((args.self_ip, args.self_port))
    server.listen(10)

    packet = open('data_backup/mh0_packet.txt', 'w')

    while True:
        connect, addr = server.accept()
        data = connect.recv(1024)
        print(data)
        packet.write("%s: %s\n" % (addr, data))
        packet.flush()
        connect.send('{}+my test.'.format(addr))
    server.close()
