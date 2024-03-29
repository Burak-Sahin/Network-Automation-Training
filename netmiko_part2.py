import netmiko    # For SSH to network elements
import json       # For dealing with dictionary-like JSON format
import net_tools  # Our own tool for getting credentials
import os         # For dealing with directories and files
import sys        # Enabling us to utilize arguments to the script


# Get username and password variables from the user
login, password = net_tools.get_credentials()

# Use 1st argument to the script to get json file with list of NEs
# This will give us a list of NEs (each as a dictionary)
with open(sys.argv[1]) as node_file:
    nodes = json.load(node_file)

# Use 2nd argument to the script to get the file with list of show commands
with open(sys.argv[2]) as cmd_file:
    commands = cmd_file.readlines()

# Create a tuple of exceptions
netmiko_exceptions = (netmiko.ssh_exception.NetMikoAuthenticationException,
                      netmiko.ssh_exception.NetMikoTimeoutException)

# Loop over each NE
for node in nodes:
    # Update each node dictionary with credentials entered by the user
    node["username"] = login
    node["password"] = password

    # Try to connect to the node to run the commands
    try:
        print("~" * 79)
        print("Connecting to the node -> {}".format(node["ip"]))

        # Create the connection to the node
        connection = netmiko.ConnectHandler(**node)

        # Get the node name using base_prompt property of the ConnectionHandler
        # In Nokia routers, this will give us a string like "A:SR1"
        # so we split this string by ":" to get the second part out of it
        node_dir = connection.base_prompt.split(":")[1]

        # Check if the folder exists. Create if it does not
        if not os.path.exists(node_dir):
            os.mkdir(node_dir)

        # For each command create a file under the directory with node name
        for cmd in commands:
            out_file = cmd.replace(' ', '_').rstrip() + ".txt"
            out_file = "\\".join((node_dir, out_file))

            # Send the command and write the output to the respective file
            with open(out_file, 'w+') as f:
                output = connection.send_command(cmd)
                f.write(output + "\n\n")
        # Close the connection to the node
        connection.disconnect()

    # Give a proper output to the user if the connection fails and keep on
    except netmiko_exceptions as e:
        print("--> FAILURE: {}".format(node["ip"], e))
