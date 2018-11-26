from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.clean import cleanup
from mininet.cli import CLI
from mininet.log import *
from mininet.node import OVSSwitch
from mininet.node import RemoteController
import time


class LinearTopo(Topo):
    "Simple topology example."
    '''
       host --- switch --- switch --- host
    '''

    def __init__(self):
        "Create custom topo."
        # Initialize topology
        Topo.__init__(self)
        # Add hosts and switches
        leftHost = self.addHost('h1')
        rightHost = self.addHost('h2')
        leftSwitch = self.addSwitch('s3')
        rightSwitch = self.addSwitch('s4')
        # Add links
        self.addLink(leftHost, leftSwitch, bw=10, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(leftSwitch, rightSwitch)
        self.addLink(rightSwitch, rightHost)


class StarTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        CenterSwitch = self.addSwitch('s0')
        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        Host4 = self.addHost('h4')
        Host5 = self.addHost('h5')

        # Add links
        self.addLink(CenterSwitch, Host1)
        self.addLink(CenterSwitch, Host2)
        self.addLink(CenterSwitch, Host3)
        self.addLink(CenterSwitch, Host4)
        self.addLink(CenterSwitch, Host5)


class RingTopo(Topo):
    "Simple topology example."

    def __init__(self, s_num=5, node_per_s=1):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)
        self.s_num = s_num
        self.node_per_s = node_per_s
        self.s_list = []
        self.node_list = []

        # Add hosts and switches
        for i in range(self.s_num):
            tmp_switch = self.addSwitch('s{}'.format(i + 1), failMode='standalne', stp=True)
            self.s_list.append(tmp_switch)
            self.node_list.append([])
            for j in range(self.node_per_s):
                tmp_node = self.addHost('h{}{}'.format(i + 1, j + 1))
                self.node_list[i].append(tmp_node)

        # Add links
        '''
        TODO: This is not a real ring topo.
              Need to be fixed with controller in topo with loop.
        '''
        for i in range(self.s_num - 1):
            self.addLink(self.s_list[i], self.s_list[0 if i + 1 == self.s_num else i + 1])
        for i in range(self.s_num):
            for j in range(self.node_per_s):
                self.addLink(self.s_list[i], self.node_list[i][j])


def test_linear_topo():
    cleanup()
    print('\n*** Linear Topo Test ***')
    net = Mininet(topo=LinearTopo(), link=TCLink)
    net.start()
    net.pingAll()
    net.stop()


def test_star_topo():
    cleanup()
    print('\n*** Star Topo Test ***')
    net = Mininet(topo=StarTopo(), link=TCLink)
    net.start()
    net.pingAll()
    net.stop()


def test_ring_topo():
    cleanup()
    print('\n*** Ring Topo Test ***')
    net = Mininet(topo=RingTopo(), link=TCLink, switch=OVSSwitch)
    net.start()
    # CLI(net)
    net.pingAll()
    net.stop()


if __name__ == '__main__':
    # setLogLevel('info')
    test_linear_topo()
    test_star_topo()
    test_ring_topo()
