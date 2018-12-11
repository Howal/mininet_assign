import json
import socket
import argparse
import time
import util_config as config
from util_socket import send_msg, recv_msg, get_self_ip
from util_block import Block
import asyncio


async def minining_based_on_PoW():
    global args, blockchain, tranxqueue, peerlist

    while True:
        # select tranx from tranxlist

        # check the tranx (this can be skipped for now)

        # use Block to get hash and check the hex result

        # check whether the hex agree with the diff-level (the number of zeros in the front)

        # simulate the computing power
        await asyncio.sleep(config.MINI_SLEEP_TIME)


async def receive_msg_and_forward():
    global args, blockchain, tranxqueue

    # bind the listening port
    node_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_in.bind((args.self_ip, config.PORT_IN))
    node_in.listen(10)

    while True:
        # accept connect
        connect, addr = await node_in.accept()
        # receive msg

        # distinguish block info or tranx info

        # update the blockchain or tranxqueue

        # forward to other node


async def update_peer_node_list():
    global args, peerlist

    while True:
        # check each element in peerlist valid or not

        # delete invalid ones

        # acquire more peer if needed
        if len(peerlist) < config.MIN_PEER_NUM:
            # get peer from bootstrapper
            continue
        await asyncio.sleep(config.UPDATE_SLEEP_TIME)


def get_init_from_bootstrapper():
    global args, blockchain, tranxqueue, peerlist
    # receive previous block and tranx

    # init peerlist
    peerlist = [args.seed_ip]
    # acquire more peer if needed
    while len(peerlist) < config.MIN_PEER_NUM:
        # get more peer from bootstrapper
        continue


def init_regular_node():
    global args, blockchain, tranxqueue, peerlist

    blockchain = []
    tranxqueue = []
    peerlist = []
    # connect to bootstrapper for block info
    get_init_from_bootstrapper()

    # setup work loop
    loop = asyncio.get_event_loop()
    tasks = [update_peer_node_list(), minining_based_on_PoW(), receive_msg_and_forward()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    global args
    parser = argparse.ArgumentParser(description='receive server help')
    parser.add_argument('--seed-ip', help='bootstapper ip', type=str)
    args = parser.parse_args()

    # get self ip
    args.self_ip = get_self_ip(args.seed_ip, config.PORT_IN)
    init_regular_node()
