import ansible_runner

def ospf_neighbors():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show ip ospf neighbor"]}',
        host_pattern="routers"  # Update with the correct host group from your inventory
    )

    # Extract and display command output
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                for output in response["stdout"]:
                    print(output)

    return output  # Return the exit code (0 means success)

def routing_table():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show ip route"]}',
        host_pattern="routers"  # Update with the correct host group from your inventory
    )

    # Extract and display command output
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                for output in response["stdout"]:
                    print(output)

    return output  # Return the exit code (0 means success)

def ospf_database():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show ip ospf database"]}',
        host_pattern="routers"  # Update with the correct host group from your inventory
    )

    # Extract and display command output
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                for output in response["stdout"]:
                    print(output)

    return output  # Return the exit code (0 means success)
