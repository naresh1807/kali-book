import ipaddress
net = ipaddress.ip_network("192.0.2.0/24")
for text in ["192.0.2.10", "198.51.100.10"]:
    print(text, ipaddress.ip_address(text) in net)
