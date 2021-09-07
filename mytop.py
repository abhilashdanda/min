
#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink, Intf,Link
from mininet.node import Controller, OVSController, OVSSwitch
from cmd import Cmd

 

#///////////////////////////////////////////////////////////////////////////////

 

class MyTopo(Topo):
    def build(self):
        c0 =self.addController('co',port =6633)
        H1 = self.addHost( 'h1' , cls=Host, defaultRoute=None)
        H2 = self.addHost( 'h2' , cls=Host, defaultRoute=None)
        
        S1 = self.addSwitch( 's1')
        S2 = self.addSwitch( 's2')

        # Add links
        self.addLink( H1, S1)


        s2s1 = {'bw' :10,'delay' : '0ms', 'loss':50, 'jitter':0}
        self.addLink( S2, S1, cls = TCLink,loss = 50 )
        
        s1s2 = {'bw' :10,'delay' : '0ms', 'loss':75, 'jitter':0}
        self.addLink( S1, S2, cls = TCLink, loss =75 )

        self.addLink( S1, H2)

 


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

 

def Run():
    print( "********starting Network********" )
    net = Mininet(Mytopo)
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














