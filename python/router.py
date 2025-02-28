import ansible_runner
import json
class Router_Facts:
    class Interface:
        def __init__(self, name, address_subnet, status,description):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status
            self.description=description


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
            self.next_hop=next_hop
            self.admin_distance=admin_distance
    def __init__(self, id, device, interfaces, neighbors,routing_tables):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors = [self.Neighbor(*neighbor) for neighbor in neighbors]  # List of Neighbor objects
        self.routing = [self.Routing(*routing_table) for routing_table in routing_tables]  # List of Neighbor objects

def Routers_facts():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/device.yaml",
    inventory="hosts",  # Path to external inventory file
    tags="routers",
    rotate_artifacts=10,        
    extravars={                              # Pass the selected role as a variable
        "target_hosts": 'routers'}
    )
    # Get the list of hosts where tasks ran
    hosts_with_tasks = [host for host in  r.stats["ok"]]
    facts = []
    # Print the hosts where tasks were executed

    for host in hosts_with_tasks:
        facts_file = "../ansible/temp/router_facts_" + host + ".json"

        with open(facts_file, "r") as f:
            router_facts = json.load(f)
        # print(router_interface_list(router_facts["net_interfaces"]))    
        routing_table_output = router_facts["routing_table"]["stdout"][0]

        facts.append(Router_Facts(id=host ,device=router_facts["net_hostname"], 
                           interfaces=router_interface_list(router_facts["net_interfaces"]),
                           neighbors=router_neighbor_list(router_facts["net_neighbors"]),
                           routing_tables=parse_routing_table(routing_table_output)))


    print (facts[0].id,
           facts[0].device , 
           facts[0].interfaces[0].name , 
           facts[0].interfaces[0].address_subnet ,
           facts[0].interfaces[0].status ,
           facts[0].interfaces[0].description ,
           facts[0].neighbors[0].name,
           facts[0].neighbors[0].address_subnet,
           facts[0].neighbors[0].port,
           facts[1].routing[1].interface,
           facts[1].routing[1].network,           
           facts[1].routing[1].protocol,
           facts[1].routing[1].next_hop,
           facts[1].routing[1].admin_distance)
    print("\n")
    # print (facts[1].id,
    #        facts[1].device , 
    #        facts[1].interfaces[1].name , 
    #        facts[1].interfaces[1].address_subnet ,
    #        facts[1].interfaces[1].status ,
    #        facts[1].neighbors[0].name,
    #        facts[1].neighbors[0].address_subnet,
    #        facts[1].neighbors[0].port)
    return facts

def router_interface_list(dict):
    temp =[]
    for i in dict:
        temp.append([
            i,
            dict[i]["ipv4"] if dict[i]["ipv4"] not in [None, ""] and dict[i]["ipv4"] != [] else "N/A",
            dict[i]["lineprotocol"] if dict[i]["lineprotocol"] not in [None, ""] else "N/A",
            dict[i]["description"] if dict[i]["description"] not in [None, ""] else "N/A"
        ])  
    return temp    

def router_neighbor_list(dict):
    temp =[]
    for i in dict:
        for j in dict[i]:
            temp.append([
                j["host"] if j.get("host") not in [None, ""] else "N/A",
                j["ip"] if j.get("ip") not in [None, ""] else "N/A",
                j["port"] if j.get("port") not in [None, ""] else "N/A"
            ])
    return temp    

def parse_routing_table(output):
    # Map protocol codes to human-readable descriptions
    protocol_map = {
        "C": "Direct Connected",
        "L": "Local",
        "S": "Static",
        "O": "OSPF",
        "O IA": "OSPF Inter-Area",
        "O E1": "OSPF External Type 1",
        "O E2": "OSPF External Type 2",
        "R": "RIP",
        "B": "BGP",
        "D": "EIGRP",
        "S*": "Default",
    }

    routes = []
    lines = output.splitlines()

    for line in lines:
        # Skip irrelevant lines
        if (
            "Gateway of last resort" in line  # Skip "Gateway of last resort" line
            or "variably subnetted" in line   # Skip "variably subnetted" lines
            or not line.strip()               # Skip empty lines
            or line.startswith("Codes:")      # Skip "Codes:" header lines
            or line.startswith(" ")           # Skip indented lines (e.g., protocol descriptions)
        ):
            continue

        # Split the line into parts
        parts = line.split()

        # Extract protocol, network, and interface
        protocol_code = parts[0].strip()
        network = parts[1]
        interface = parts[-1]  # Interface is always the last part

        # Handle next hop (if present)
        next_hop = "N/A"
        if "via" in parts:
            via_index = parts.index("via")
            next_hop = parts[via_index + 1]

        # Handle admin distance and metric (if present)
        admin_distance = "N/A"
        if "[" in line:
            admin_distance = line.split("[")[1].split("/")[0]

        # Map protocol code to human-readable description
        protocol = protocol_map.get(protocol_code, f"Unknown ({protocol_code})")

        # Append the parsed data as a list
        routes.append([
            protocol,
            network,
            interface,
            next_hop,
            admin_distance
        ])

    return routes

# Routers_facts()
