
#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink, Intf,Link
from cmd import Cmd
from mininet.node import Controller, OVSController, OVSSwitch

 

#///////////////////////////////////////////////////////////////////////////////

 

class LinearTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=4):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2')
        l1=self.addLink(h1, s1,port1=1,port2=1)
        l2=self.addLink(h2, s2,port1=1,port2=1)
        lf=self.addLink(s1,s2,port1=2,port2=2, cls=TCLink , jitter='20ms')
        l4=self.addLink(s1,s2, port1=3,port2=3,cls=TCLink ,latency_ms=100 )

 


#////////////////////////////////////////////////////////////////////////////////////
class User(CLI):

 

    def do_a( self, line ):
        s1=self.mn.get('s1')
        s2=self.mn.get('s2')
        links=self.mn.linksBetween(s1,s2)
        links[0].intf1.config( latency_ms='22')

 

        
        

 

    def do_d( self, line ):
        s1=self.mn.get('s1')
        s2=self.mn.get('s2')
        links=self.mn.linksBetween(s1,s2)
        links[0].intf1.config( latency_ms='18')
        
       
    def do_q( self, line ):
        return self.do_exit( line )
                 
#////////////////////////////////////////////////////////////////////////////

 

def simpleTest():
    print( "********starting Network********" )
    topo = LinearTopo(n=2)
    net = Mininet(topo)
    net.start()
    
    c0=net.get('c0')

 

    c0.cmd("ovs-ofctl add-flow s1 in_port:2,actions=drop")
    c0.cmd("ovs-ofctl add-flow s1 ,in_port=1,action=output=2")
    c0.cmd("ovs-ofctl add-flow s1 ,in_port=3,action=output=1")
    c0.cmd("ovs-ofctl add-flow s2 in_port:3,actions=drop")
    c0.cmd("ovs-ofctl add-flow s2 ,in_port=1,action=output=3")
    c0.cmd("ovs-ofctl add-flow s2 ,in_port=2,action=output=1")

 

    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)

 

    print("Enter a-> To increase ")
    print("Enter d-> To decrease ")
    print("Enter q-> To Terminate  ")

 

    User(net)
    net.stop()

 

#/////////////////////////////////////////////////////////////////////////////    

 

if __name__ == '__main__':
    
    setLogLevel('info')
    simpleTest()
    
#///////////////////////////////////////////////////////////////////////////////














