import json
import socket
import argparse
import time
import util_config as config
from util_socket import send_msg, recv_msg, get_self_ip
from util_block import Block
import asyncio


# Mengyang TODO
async def minining_based_on_PoW():
    global args, blockchain, tranxqueue, peerlist

    while True:
        # select tranx from tranxqueue

        # check the tranx (this can be skipped for now)

        # use Block to get hash and check the hex result

        # check whether the hex agree with the diff-level (the number of zeros in the front)

        # simulate the computing power
        await asyncio.sleep(config.MINI_SLEEP_TIME)


# Ende TODO
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
        raw_data = recv_msg(connect)
        # distinguish block info or tranx info
        if raw_data == '#TRANX':
            # tranx
            continue
        elif raw_data == '#BLOCK':
            # block
            continue
        elif raw_data == '#PEERCHECK':
            # this is used for valid node check
            # no need to write any code here
            continue
        # update the blockchain or tranxqueue

        # forward to other node


async def update_peer_node_list():
    global args, peerlist

    while True:
        peer_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # check each element in peerlist valid or not
        for ip_tmp in peerlist:
            try:
                peer_out.connect_ex((ip_tmp, config.PORT_IN))
            except Exception as e:
                print(e)
                # delete invalid ones
                peerlist.remove(ip_tmp)
            else:
                send_msg(peer_out, '#PEERCHECK')
            finally:
                peer_out.close()
        # acquire more peer if needed
        if len(peerlist) < config.MIN_PEER_NUM:
            # get peer from bootstrapper
            peer_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_out.connect_ex((args.seed_ip, config.PORT_IN))
            send_msg(peer_out, '#PEER')
            tmp_ip = recv_msg(peer_out)
            if tmp_ip not in peerlist:
                peerlist.append(tmp_ip)
            peer_out.close()

        await asyncio.sleep(config.UPDATE_SLEEP_TIME)


def get_init_from_bootstrapper():
    global args, blockchain, tranxqueue, peerlist
    # receive previous block and tranx

    # init peerlist
    peerlist = [args.seed_ip]

    init_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    init_out.connect_ex((args.seed_ip, config.PORT_IN))
    send_msg(init_out, '#INIT')
    raw_data = recv_msg(init_out)
    tmp_data = json.loads(raw_data)
    blockchain = tmp_data[0]
    tranxqueue = tmp_data[1]
    init_out.close()


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
