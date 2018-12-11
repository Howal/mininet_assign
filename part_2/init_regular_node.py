import json
import socket
import argparse
import time
import util_config as config
from util_socket import send_msg, recv_msg, get_self_ip


def minining_based_on_PoW():
    return


def receive_block_and_forward():
    return


def receive_trax_and_forward():
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='receive server help')
    parser.add_argument('--seed-ip', help='ip', default='10.0.0.99', type=str)
    args = parser.parse_args()

    # get self ip
    args.self_ip = get_self_ip(args.seed_ip, config.PORT_IN)
