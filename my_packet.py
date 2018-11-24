from mininet.net import Mininet
from mininet.link import TCLink
from my_topo import LinearTopo, StarTopo, RingTopo
import time


def test_packet_topo():
    print('\n*** Linear Topo Test ***')
    net = Mininet(topo=LinearTopo(), link=TCLink)
    net.start()
    net.pingAll()

    print('---my test---')
    h1 = net.get('h1')
    h2 = net.get('h2')
    print(h1.IP(), h2.IP())

    h1.sendCmd('python receive_packet.py --ip {} &'.format(h1.IP()))
    _tmp_result = h1.waitOutput()

    h2.sendCmd('sudo python send_packet.py --ip {} --data {}'.format(h1.IP(), "\'hello world!\'"))
    _tmp_result = h2.waitOutput()
    h2.sendCmd('python send_packet.py --ip {} --data {}'.format(h1.IP(), "my_test."))
    _tmp_result = h2.waitOutput()
    h2.sendCmd('python send_packet.py --ip {} --data {}'.format(h1.IP(), "my_test2"))
    _tmp_result = h2.waitOutput()

    # make sure h1 got the final msg
    time.sleep(5)
    h1.cmd('kill %python')

    print('---my test down---')
    net.stop()


if __name__ == '__main__':
    test_packet_topo()
