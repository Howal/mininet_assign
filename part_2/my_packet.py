from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.clean import cleanup
from mininet.cli import CLI
from mininet.util import pmonitor
from mininet.log import *
import time


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


def test_packet_topo():
    # ----------- test start -------------
    cleanup()
    computing_hosts_num = 3

    # ----------- set topo -----------
    net = Mininet(topo=StarTopo(computing_hosts_num), link=TCLink)

    # ----------- init net -------------
    net.start()
    # first test
    # CLI(net)
    net.pingAll()

    mh0 = net.get('mh0')
    mh0.cmd('python monitor_node_init.py --self-ip {} &'.format(mh0.IP()))

    for i in range(computing_hosts_num):
        tmp_h = net.get('ch{}'.format(i + 1))
        tmp_h.cmd('python computing_node_init.py --seed-ip {} &'.format(mh0.IP()))
    print("----- start monitor ----- \n")
    # net.startTerms()
    while True:
        print(mh0.monitor())
        # print(tmp_h.monitor())

    '''
    mh0.sendCmd('sudo python net_init/monitor_node_init.py &')
    # use monitor host as hard-code seed in Bitcoin
    for tmp_h in ch_list:
        tmp_h.sendCmd('sudo python net_init/computing_node_init.py --ip {} &'.format(mh0.IP()))
        _tmp_result = tmp_h.waitOutput(verbose=False)
    '''
    '''
    h1.sendCmd('python receive_packet.py --ip {} &'.format(h1.IP()))
    _tmp_result = h1.waitOutput()
    h2.sendCmd('sudo python send_packet.py --ip {} --data {}'.format(h1.IP(), "\'hello world!\'"))
    _tmp_result = h2.waitOutput()
    h2.sendCmd('python send_packet.py --ip {} --data {}'.format(h1.IP(), "my_test."))
    _tmp_result = h2.waitOutput()
    h2.sendCmd('python send_packet.py --ip {} --data {}'.format(h1.IP(), "my_test2"))
    _tmp_result = h2.waitOutput()
    '''

    # make sure h1 got the final msg
    time.sleep(5)
    mh0.cmd('kill %python')
    tmp_h.cmd('kill %python')
    # ---------- test stop ------------
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    test_packet_topo()
