from mininet.net import Mininet
from mininet.link import TCLink
from mininet.clean import cleanup
import time


def test_packet_topo():
    # ----------- test start -------------
    cleanup()
    net = Mininet(link=TCLink)

    # ----------- set topo -----------
    # add center switch
    s0 = net.addSwitch('s0', ip='10.0.0.255')
    # add monitoring host
    mh0 = net.addHost('mh0', ip='10.0.0.100')
    # add computing hosts
    computing_hosts_num = 10
    ch_list = []
    for i in range(computing_hosts_num):
        tmp_h = net.addHost('ch{}'.format(i), ip='10.0.0.{}'.format(i))
        ch_list.append(tmp_h)
    # add links
    net.addLink(s0, mh0)
    for tmp_h in ch_list:
        net.addLink(s0, tmp_h)

    # ----------- init net -------------
    net.build()
    net.start()
    # first test
    net.pingAll()
    s0.sendCmd('sudo python net_init/monitor_node_init.py &')
    # use monitor host as hard-code seed in Bitcoin
    for tmp_h in ch_list:
        tmp_h.sendCmd('sudo python net_init/computing_node_init.py --ip {} &'.format(mh0.IP()))
        _tmp_result = tmp_h.waitOutput(verbose=False)

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
    for tmp_h in ch_list:
        tmp_h.cmd('kill %python')
    mh0.cmd('kill %python')
    # ---------- test stop ------------
    net.stop()


if __name__ == '__main__':
    test_packet_topo()
