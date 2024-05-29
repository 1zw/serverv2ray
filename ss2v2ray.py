import base64
import json
import re

def decode_ss_uri(uri):
    match = re.match(r'ss://([a-zA-Z0-9+/=]+)@([^:]+):(\d+)#(.+)', uri)
    if match:
        method_password = base64.urlsafe_b64decode(match.group(1)).decode('utf-8')
        method, password = method_password.split(':', 1)
        address = match.group(2)
        port = int(match.group(3))
        remarks = match.group(4)
        return {
            'address': address,
            'port': port,
            'method': method,
            'password': password,
            'remarks': remarks
        }
    return None

def generate_v2ray_config(servers):
    config = {
        "inbounds": [
            {
                "port": 1080,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {
                    "auth": "noauth",
                    "udp": True
                }
            }
        ],
        "outbounds": [],
        "routing": {
            "rules": []
        }
    }

    for i, server in enumerate(servers):
        outbound = {
            "protocol": "shadowsocks",
            "settings": {
                "servers": [
                    {
                        "address": server['address'],
                        "port": server['port'],
                        "method": server['method'],
                        "password": server['password']
                    }
                ]
            },
            "tag": f"server{i+1}"
        }
        config["outbounds"].append(outbound)
    
    return config

def main():
    servers = []
    with open('subscription.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                server = decode_ss_uri(line)
                if server:
                    servers.append(server)

    v2ray_config = generate_v2ray_config(servers)
    
    with open('config.json', 'w') as file:
        json.dump(v2ray_config, file, indent=4)

if __name__ == '__main__':
    main()
