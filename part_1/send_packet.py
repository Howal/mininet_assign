import socket
import argparse

parser = argparse.ArgumentParser(description='send once help')
parser.add_argument('--ip', help='', default='127.0.0.1', type=str)
parser.add_argument('--port', help='', default=12345, type=int)
parser.add_argument('--data', help='', type=str)
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(args.data, (args.ip, args.port))
