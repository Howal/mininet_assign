from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.clean import cleanup
from mininet.cli import CLI
from mininet.util import pmonitor
from mininet.log import setLogLevel
import time
import os


def my_cleanup():
    # clear process
    os.system("pkill %python3")
    # mininet cleanup
    cleanup()


class StarTopo(Topo):
    "Simple topology example."

    def __init__(self, computing_hosts_num=5):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        self.computing_hosts_num = computing_hosts_num
        self.ch_list = []

        # add center switch
        s0 = self.addSwitch('s0', ip='10.0.0.255')
        # add monitoring host
        mh0 = self.addHost('mh0', ip='10.0.0.100')
        # add computing hosts
        for i in range(self.computing_hosts_num):
            tmp_h = self.addHost('ch{}'.format(i + 1), ip='10.0.0.{}'.format(i + 1))
            self.ch_list.append(tmp_h)
        # add links
        self.addLink(s0, mh0)
        for tmp_h in self.ch_list:
            self.addLink(s0, tmp_h)


def start_mininet():
    # ----------- start -------------
    my_cleanup()
    computing_hosts_num = 3

    # ----------- set topo -----------
    net = Mininet(topo=StarTopo(computing_hosts_num), link=TCLink)

    # ----------- init net -------------
    net.start()
    # CLI(net)
    # net.startTerms()
    net.pingAll()

    mh0 = net.get('mh0')
    mh0.cmd('python3 init_monitor_node.py --self-ip {} &'.format(mh0.IP()))

    for i in range(computing_hosts_num):
        tmp_h = net.get('ch{}'.format(i + 1))
        tmp_h.cmd('python3 init_regular_node.py -seed-ip {} &'.format(mh0.IP()))

    print("----- start monitor ----- \n")
    while True:
        print(mh0.monitor())

    # ---------- test stop ------------
    time.sleep(5)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    start_mininet()
