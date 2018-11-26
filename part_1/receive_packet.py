import socket
import argparse

parser = argparse.ArgumentParser(description='receive server help')

parser.add_argument('--ip', help='ip', default='127.0.0.1', type=str)
parser.add_argument('--port', help='port', default=12345, type=int)
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((args.ip, args.port))


f = open('h1_foo.txt', 'w')
while True:
    data, addr = s.recvfrom(512)
    f.write("%s: %s\n" % (addr, data))
    f.flush()
