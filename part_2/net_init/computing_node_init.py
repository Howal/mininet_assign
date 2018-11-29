import socket
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='receive server help')

    parser.add_argument('--self-ip', help='ip', default='localhost', type=str)
    parser.add_argument('--self-port', help='port', default=12345, type=int)
    parser.add_argument('--seed-ip', help='ip', default='10.0.0.99', type=str)
    parser.add_argument('--seed-port', help='port', default=12345, type=int)
    args = parser.parse_args()
    print(args.seed_ip)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind((args.self_ip, args.self_port))
    # s.listen(10)
    client.connect((args.seed_ip, args.seed_port))
    while True:
        client.send('hello! from client!')
        data = client.recv(1024)
        print(data)
        time.sleep(1)
    client.close()

    # while True:
    #     conn, addr = s.accept()
    #     data = conn.recv(1024)
    #     packet.write("%s: %s\n" % (addr, data))
    #     packet.flush()
    #     conn.send('{}'.format(addr))
    # s.close()
