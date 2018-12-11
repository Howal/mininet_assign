import json
import socket
import argparse
import time
import util_config as config
from util_socket import send_msg, recv_msg, get_self_ip
from util_block import Block, create_genesis_block
import asyncio


async def send_pseudo_tranx():
    global args, blockchain, tranxqueue, peerlist

    while True:
        # send pseudo tranx with dummy data for function test
        await asyncio.sleep(60)


async def node_logger():
    global args, blockchain, tranxqueue, peerlist

    while True:
        # decide what to write and how to arrange the result
        packet = open('{}/monitor.txt'.format(config.LOG_DIR), 'w')
        packet.write("dummy")
        packet.flush()
        await asyncio.sleep(60)


async def reply_all_request():
    global args, blockchain, tranxqueue, peerlist

    node_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_in.bind((args.self_ip, args.self_port_in))
    node_in.listen(30)

    while True:
        # wait for connection
        connect, addr = await node_in.accept()
        # use raw_data to distinguish what kind of tasks
        raw_data = recv_msg(connect)
        # init
        if raw_data == '#INIT':
            if addr[0] not in peerlist:
                peerlist.append(addr[0])
            send_msg(connect, '#IPLIST#{}'.format(json.dumps(peerlist)))
        # update peer list
        elif raw_data == '#PEER':
            return
        # receive tranx
        elif raw_data == '#TRANX':
            return
        # receive block
        elif raw_data == '#BLOCK':
            return
        # else?
        else:
            continue
        connect.close()

    node_in.close()


async def update_peer_node_list():
    global args, peerlist

    while True:
        # check each element in peerlist valid or not

        # delete invalid ones

        # wait for a moment
        await asyncio.sleep(config.UPDATE_SLEEP_TIME)


def init_monitor_node():
    global args, blockchain, tranxqueue, peerlist

    blockchain = [create_genesis_block()]
    tranxqueue = []
    peerlist = []

    loop = asyncio.get_event_loop()
    tasks = [update_peer_node_list(), reply_all_request(), node_logger()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    global args
    parser = argparse.ArgumentParser(description='receive server help')
    parser.add_argument('--self-ip', help='ip', default='localhost', type=str)
    args = parser.parse_args()

    init_monitor_node()
