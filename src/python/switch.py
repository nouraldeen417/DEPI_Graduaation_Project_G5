import ansible_runner
import json
import re

class Switch_Facts:
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

def switches_facts():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/device.yaml",
    inventory="hosts",  # Path to external inventory file
    tags="switches",
    rotate_artifacts=10,
    extravars={                              # Pass the selected role as a variable
        "target_hosts": 'switches'}
    )
    # Get the list of hosts where tasks ran
    hosts_with_tasks = [host for host in  r.stats["ok"]]
    facts = []
    # Print the hosts where tasks were executed

    for host in hosts_with_tasks:
        facts_file = "../ansible/temp/switch_facts_" + host + ".json"

        with open(facts_file, "r") as f:
            router_facts = json.load(f)
        vlan_output = router_facts["vlans"]["stdout"][0]
        facts.append(Switch_Facts(id=host ,device=router_facts["net_hostname"], 
                           interfaces=switch_interface_list(router_facts["net_interfaces"]),
                           neighbors=switch_neighbor_list(router_facts["net_neighbors"]),
                           vlans=parse_vlan_table(vlan_output)))
                        
    print (facts[0].id,
           facts[0].device , 
           facts[0].interfaces[0].name , 
           facts[0].interfaces[0].address_subnet ,
           facts[0].interfaces[0].status ,
           facts[0].interfaces[0].description ,
           facts[0].neighbors[0].name,
           facts[0].neighbors[0].address_subnet,
           facts[0].neighbors[0].port,
           facts[0].vlans[0].id,
           facts[0].vlans[0].name,
           facts[0].vlans[0].status,
           facts[0].vlans[0].port)
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

def switch_interface_list(dict):
    temp =[]
    for i in dict:
        temp.append([
            i,
            dict[i]["ipv4"] if dict[i]["ipv4"] not in [None, ""] and dict[i]["ipv4"] != [] else "N/A",
            dict[i]["lineprotocol"] if dict[i]["lineprotocol"] not in [None, ""] else "N/A",
            dict[i]["description"] if dict[i]["description"] not in [None, ""] else "N/A"
        ])  
    return temp    

def switch_neighbor_list(dict):
    temp =[]
    for i in dict:
        for j in dict[i]:
            temp.append([
                j["host"] if j.get("host") not in [None, ""] else "N/A",
                j["ip"] if j.get("ip") not in [None, ""] else "N/A",
                j["port"] if j.get("port") not in [None, ""] else "N/A"
            ])
    return temp    

def parse_vlan_table(output):
    # Initialize a list to store VLAN information
    vlans = []
    
    # Split the output into lines
    lines = output.splitlines()

    # Temporary variable to track the current VLAN
    current_vlan = None

    for line in lines:
        # Skip lines that are part of the header or footer
        if (
            "VLAN Name" in line  # Skip header line
            or "----" in line    # Skip separator line
            or not line.strip()  # Skip empty lines
        ):
            continue

        # Split the line into parts
        parts = line.split()

        # Check if the line is a VLAN entry
        if parts[0].isdigit():  # VLAN ID is numeric
            # If there's a current VLAN being processed, add it to the list
            if current_vlan:
                vlans.append(current_vlan)

            # Start a new VLAN entry
            vlan_id = int(parts[0])  # VLAN ID
            name = parts[1]          # VLAN Name
            status = parts[2]        # Status
            ports = " ".join(parts[3:]).strip()  # Ports (join remaining parts)
            if ports == "" :
                ports = "N/A"
                
            current_vlan = [vlan_id, name, status, ports]
        else:
            # If the line doesn't start with a VLAN ID, it's a continuation of ports for the current VLAN
            if current_vlan and line.strip():
                current_vlan[3] += ' ' + line.strip()

    # Add the last VLAN entry to the list
    if current_vlan:
        vlans.append(current_vlan)

    return vlans

# switches_facts()