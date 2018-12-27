import json
import socket
import argparse
import time
import util_config as config
from util_socket import send_msg, recv_msg
from util_block import Block, create_genesis_block
import asyncio
import random
import datetime as date


async def send_pseudo_tranx():
    global args, blockchain, tranxqueue, peerlist

    while True:
        # send pseudo tranx with dummy data for function test
        tranx_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tranx_out.connect_ex((peerlist[random.randint(0, len(peerlist) - 1)], config.PORT_IN))
        send_msg(tranx_out, '#TRANX')
        send_msg(tranx_out, 'dummy_tranx_{}'.format(date.datetime.time()))
        tranx_out.close()
        await asyncio.sleep(60)


async def node_logger():
    global args, blockchain, tranxqueue, peerlist

    while True:
        # decide what to write and how to arrange the result
        packet = open('{}/blockchain_{}.txt'.format(config.LOG_DIR, date.datetime.now()), 'w')
        packet.write('{}'.format(json.dumps(blockchain)))
        packet.flush()
        packet = open('{}/tranxqueue_{}.txt'.format(config.LOG_DIR, date.datetime.now()), 'w')
        packet.write('{}'.format(json.dumps(tranxqueue)))
        packet.flush()
        packet = open('{}/peerlist_{}.txt'.format(config.LOG_DIR, date.datetime.now()), 'w')
        packet.write('{}'.format(json.dumps(peerlist)))
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
            send_msg(connect, '{}'.format(json.dumps([blockchain, tranxqueue])))

        # Ende TODO
        # receive tranx
        elif raw_data == '#TRANX':
            # tranx
            tranx = recv_msg(connect)
            if tranx not in tranxqueue:
                # update the tranxqueue
                tranxqueue.append(tranx)
                # forward to other node
                for ele in peerlist:
                    tranx_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    tranx_out.connect_ex((ele, config.PORT_IN))
                    send_msg(tranx_out, '#TRANX')
                    send_msg(tranx_out, tranx)
                    tranx_out.close()
            continue
        # receive block
        elif raw_data == '#BLOCK':
            # block
            raw_data = recv_msg(connect)
            block = json.loads(raw_data)
            # check
            if block.index > blockchain[-1].index and block.hash_block().startswith(config.HASH_HARD):
                # update the blockchain
                blockchain.append(block)
                for ele in peerlist:
                    # forward to other node
                    block_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    block_out.connect_ex((ele, config.PORT_IN))
                    send_msg(block_out, '#BLOCK')
                    send_msg(block_out, block)
                    block_out.close()
            continue

        # update peer list
        elif raw_data == '#PEER':
            ip_tmp = addr[0]
            while ip_tmp == addr[0]:
                ip_tmp = peerlist[random.randint(0, len(peerlist) - 1)]
            send_msg(connect, ip_tmp)
        # else?
        else:
            continue
        connect.close()

    node_in.close()


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
