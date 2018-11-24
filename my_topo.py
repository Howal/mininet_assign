from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink


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

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        Host4 = self.addHost('h4')
        Host5 = self.addHost('h5')

        # Add links
        self.addLink(Host1, Host2)
        self.addLink(Host2, Host3)
        self.addLink(Host3, Host4)
        self.addLink(Host4, Host5)
        self.addLink(Host5, Host1)


def test_linear_topo():
    print('\n*** Linear Topo Test ***')
    net = Mininet(topo=LinearTopo(), link=TCLink)
    net.start()
    net.pingAll()
    net.stop()


def test_star_topo():
    print('\n*** Star Topo Test ***')
    net = Mininet(topo=StarTopo(), link=TCLink)
    net.start()
    net.pingAll()
    net.stop()


def test_ring_topo():
    print('\n*** Ring Topo Test ***')
    net = Mininet(topo=RingTopo(), link=TCLink)
    net.start()
    net.pingAll()
    net.stop()


if __name__ == '__main__':
    test_linear_topo()
    test_star_topo()
    test_ring_topo()
