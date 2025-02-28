# utils.py
import sys
import random
# Add the path to the 'python' folder to the system path
sys.path.append("..")
# Now import 'some_file' from the 'python' directory
#from python import hello,router,configration,switch
class AutomationMethods:
    @staticmethod
    
    def Ping():
        status=AutomationMethodsData.Ping() #status has three lists host-ip list[], status list[] ,task name list[]
        print(status)
        return  status

    def Router_list():
        Fact_data=AutomationMethodsData.Routers_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]        
        print(Fact_data)
        return  Fact_data
    
    def Switch_list():
        Fact_data=AutomationMethodsData.switches_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]
        print(Fact_data)
        return Fact_data

    def Set_Hostname(selected_host,hostname):
        status = "ok"#configration.set_hostname(selected_host,hostname) #"ok"
        print (status)
        return status
    
    def Set_Banner(selected_host,banner):
        status = "ok"#configration.set_banner(selected_host,banner) #"ok"
        return status
    
    def set_interfaceconfigration(selected_host,interface_name,ipv4):
        print("sucess")
        print(selected_host)
        print(interface_name)
        print(ipv4)
        status = "ok"#configration.set_interfaceconfigration(selected_host,interface_name,ipv4) #"ok"
        print(status)
        return status
    

    def Ospf_routing(selected_hosts,interface_name,cidr_list, 
                     ospf_process_id, router_id, area_id,
                     hello_timer, dead_timer,tag):
        # status = configration.set_ospfconfigration((selected_hosts,interface_name,cidr_list, 
        #                  ospf_process_id, router_id, area_id,
        #                  hello_timer, dead_timer,tag))
        status = "ok"
        print(status)
        return status
    """
    selected_hosts, ----->one router selected or more must be list 
                        number of arguemnets depend on one device selected or more
    interface_name, ----->interfaces of selected router or routers (dropdown menue)
    cidr_list,------> list of ip/subnet 192.168.1.0/24,192.168.2.0/24 comma seprated 
    ospf_process_id,-----> any value 
    router_id, any value
    area_id, any value
    hello_timer,any value
    dead_timer,any value
    tag ----> i give it default value "add_configration" if user click remove configration make its value "remove_configration" 
    """
                                                               
    def Static_routing(selected_hosts, cidrs,next_hop,admin_distance,tag):
        # status = configration.set_static_routing(selected_hosts, cidrs,next_hop,admin_distance,tag)
        status = "ok"
        print(status)
        return status
    """
    selected_hosts, ----->one router only not supported multi device configration 
    cidrs------> list of ip/subnet 192.168.1.0/24,192.168.2.0/24 comma seprated 
    ospf_process_id,-----> any value 
    next_hop, ip
    admin_distance, any value
    tag ----> i give it default value "add_configration" if user click remove configration make its value "remove_configration" 
    """

    def Vlans_configs(selected_hosts,interfaces_list,vlan_cidr, 
                         vlan_id, vlan_name,tag):
        # status = configration.set_valnconfigration(selected_hosts,interfaces_list,vlan_cidr, 
        #                  vlan_id, vlan_name,tag)
        status = "ok"
        print(status)
        return status
    """
    selected_hosts, ----->one switch selected or more must be list 
                         number of arguemnets depend on one device selected or more
    interfaces_list, ----->interfaces must be list (allow to select more than interface)
    vlan_cidr,------> ip/subnet
    vlan_id,  -----> any value 
    vlan_name, any value
    tag ----> i give it default value "add_configration" ,if user click remove configration make its value "remove_configration" 
    """















#MY Data I used to Test 
class AutomationMethodsData:
    @staticmethod
    def Ping():
        # Here you can add your processing logic
        devices = []
        
        # First device
        d1 = Device(host="device1", task="task1", status="Running")
        devices.append(d1)
        
        # Second device
        d2 = Device(host="device2", task="task2", status="Stopped")
        devices.append(d2)
        return devices
    
    def Routers_facts():
        interfaces = [
            ("GigabitEthernet0/1", "192.168.1.1/24", "up", "Connection to Core Switch"),
            ("GigabitEthernet0/2", "192.168.2.1/24", "down", "Connection to Server"),
            ("GigabitEthernet0/3", "192.168.3.1/24", "up", "Connection to Access Point")
        ]

        # Dummy data for neighbors
        neighbors = [
            ("CoreSwitch", "192.168.1.2/24", "GigabitEthernet0/1"),
            ("Server", "192.168.2.2/24", "GigabitEthernet0/2"),
            ("AccessPoint", "192.168.3.2/24", "GigabitEthernet0/3")
        ]

        # Dummy data for routing tables
        routing_tables = [
            ("OSPF", "192.168.1.0/24", "GigabitEthernet0/1", "192.168.1.254", 110),
            ("Static", "192.168.2.0/24", "GigabitEthernet0/2", "192.168.2.254", 1),
            ("BGP", "192.168.3.0/24", "GigabitEthernet0/3", "192.168.3.254", 20)
        ]
        routers=[]
        routers.append(Facts(
            id="router-1",
            device="Router1",
            interfaces=interfaces,
            neighbors=neighbors,
            routing_tables=routing_tables
        ))
        routers.append(Facts(
            id="router-2",
            device="Router2",
            interfaces=interfaces,
            neighbors=neighbors,
            routing_tables=routing_tables
        ))
        # Create and return a Facts instance with dummy data
        return routers

    def switches_facts():
        # Here you can add your processing logic
        Switches = []
        # Dummy data for interfaces
        interfaces = [
            ("GigabitEthernet0/1", "192.168.1.1/24", "up", "Connection to Core Switch"),
            ("GigabitEthernet0/2", "192.168.2.1/24", "down", "Connection to Server"),
            ("GigabitEthernet0/3", "192.168.3.1/24", "up", "Connection to Access Point")
        ]

        # Dummy data for neighbors
        neighbors = [
            ("CoreSwitch", "192.168.1.2/24", "GigabitEthernet0/1"),
            ("Server", "192.168.2.2/24", "GigabitEthernet0/2"),
            ("AccessPoint", "192.168.3.2/24", "GigabitEthernet0/3")
        ]

        # Dummy data for vlans
        vlans = [
            (10, "VLAN10", "active", "GigabitEthernet0/1"),
            (20, "VLAN20", "active", "GigabitEthernet0/2"),
            (30, "VLAN30", "inactive", "GigabitEthernet0/3")
        ]
        Switches.append(Switch_Facts(
            id="swith1",
            device="Switch1",
            interfaces=interfaces,
            neighbors=neighbors,
            vlans=vlans
        ))
        Switches.append(Switch_Facts(
            id='swith2',
            device="Switch2",
            interfaces=interfaces,
            neighbors=neighbors,
            vlans=vlans
        ))
        print(Switches)
        return Switches
    
    def Firewalls_facts():
        # Here you can add your processing logic
        firewalls = []
        
        # First device
        d1 = Firewall(name="Firewall1" , ip="192.167.0.1",loc="home",stat="Stopped")
        firewalls.append(d1)
        
        # Second device
        d2 = Firewall(name="Firewall2" , ip="192.167.0.1",loc="home",stat="Running")
        firewalls.append(d2)
        return firewalls
    
class Device:
    def __init__(self, host, task, status):
        self.host = host
        self.task = task
        self.status = status
        

class Firewall:
    def __init__(self, name, ip, loc,stat):
        self.name = name
        self.ip_address=ip
        self.location=loc,
        self.status=stat
        
class Facts:
    class Interface:
        def __init__(self, name, address_subnet, status,description):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status
            self.description=description #new data


    class Neighbor:
        def __init__(self, name, address_subnet ,port):
            self.name = name
            self.address_subnet = address_subnet
            self.port = port

    class Routing:
        def __init__(self, protocol, net ,intf,next_hop,admin_distance):
            self.protocol = protocol
            self.network = net
            self.interface = intf
            self.next_hop=next_hop #new data
            self.admin_distance=admin_distance #new data
    def __init__(self, id, device, interfaces, neighbors,routing_tables):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors = [self.Neighbor(*neighbor) for neighbor in neighbors]  # List of Neighbor objects
        self.routing = [self.Routing(*routing_table) for routing_table in routing_tables]  # List of Neighbor objects

#switch_fact
class Switch_Facts:
    class Interface:
        def __init__(self, name, address_subnet, status,description):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status
            self.description=description #new data


    class Neighbor:
        def __init__(self, name, address_subnet ,port):
            self.name = name
            self.address_subnet = address_subnet
            self.port = port

    class Vlan:
        def __init__(self, id, name ,status,port):
            self.id = id
            self.name = name
            self.status = status
            self.port=port

    def __init__(self, id, device, interfaces, neighbors,vlans):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors  = [self.Neighbor(*neighbor) for neighbor in neighbors]      # List of Neighbor objects
        self.vlans      = [self.Vlan(*vlan) for vlan in vlans]                      # List of Neighbor objects
