import socket
import base64
import time
import ssl

def color_red(text):
    red = "\033[31m"
    reset = "\033[0m"
    return f"{red}{text}{reset}"

def h2_req(host, port):
    h2_payload = b'\x00'
    encoded_settings = base64.urlsafe_b64encode(h2_payload).decode('utf-8').rstrip('=')
    request = f"GET / HTTP/1.1\r\n" \
              f"Host: {host}\r\n" \
              f"Connection: Upgrade, HTTP2-Settings\r\n" \
              f"Upgrade: h2c\r\n" \
              f"HTTP2-Settings: {encoded_settings}\r\n" \
              f"\r\n"
    return request

def h2_req_https(host, port):
    h2_payload = b'\x00'
    encoded_settings = base64.urlsafe_b64encode(h2_payload).decode('utf-8').rstrip('=')
    request = f"GET / HTTP/1.1\r\n" \
              f"Host: {host}\r\n" \
              f"Connection: Upgrade, HTTP2-Settings\r\n" \
              f"Upgrade: h2\r\n" \
              f"HTTP2-Settings: {encoded_settings}\r\n" \
              f"\r\n"
    return request

def check_ver(host, port):
    request = f":method: GET\r\n" \
              f":path: /\r\n" \
              f":scheme: https\r\n" \
              f":authority: {host}\r\n"
    return request

def check_ver_http(host, port):
    request = f":method: GET\r\n" \
              f":path: /\r\n" \
              f":scheme: http\r\n" \
              f":authority: {host}\r\n"
    return request

def check_h2(host, port, timeout, connection_type):
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            if connection_type == '1': 
                request = h2_req(host, port)
            elif connection_type == '2': 
                sock = context.wrap_socket(sock, server_hostname=host)
                request = h2_req_https(host, port)
            else:
                print(color_red("Invalid connection type."))
                return
            
            sock.sendall(request.encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            print(color_red("""   
       
Response from h2 upgrade request: 
"""))
            print(response)

            if connection_type == '1':
                ver_request = check_ver_http(host, port)
                sock.sendall(ver_request.encode('utf-8'))
                ver_response = sock.recv(4096).decode('utf-8')
                print(color_red("""

Response from h2 formatted packet: 
"""))
                print(ver_response)
            else:
                ver_request = check_ver(host, port)
                sock.sendall(ver_request.encode('utf-8'))
                ver_response = sock.recv(4096).decode('utf-8')
                print(color_red("""

Response from h2 formatted packet: 
"""))
                print(ver_response)

        except socket.timeout:
            print(color_red("Request timed out."))
        except Exception as e:
            print(color_red(f"An error occurred: {e}"))
print(color_red("""
 __   __  _______         _______  _______  _______  __    _ 
|  | |  ||       |       |       ||       ||   _   ||  |  | |
|  |_|  ||____   | ____  |  _____||       ||  |_|  ||   |_| |
|       | ____|  ||____| | |_____ |       ||       ||       |
|       || ______|       |_____  ||      _||       ||  _    |
|   _   || |_____         _____| ||     |_ |   _   || | |   |
|__| |__||_______|       |_______||_______||__| |__||_|  |__|

This tool checks if a server is capable of handling requests 
over HTTP/2. It will send 2 packets. The first packet is 
a request to upgrade the connection to HTTP/2. The second 
packet sent is a request formatted in a way that is specific
to HTTP/2. If you get no response from server after 2nd packet 
is sent or if you get a "connection closed" message, it is 
likely the server does not support HTTP/2. If you do receive a 
server response, the server does support HTTP/2. This may not 
always be 100% accurate but in many cases it will help to 
identify HTTP/2 capable servers.
"""))
connection_type = input(color_red("""Choose connection type: 
1. HTTP
2. HTTPS 
""")).strip()
url = input(color_red("Enter target URL (without http:// or https://): ")).strip()

if connection_type == '1':
    port = 80
    port_input = input(color_red("Enter target port (or press Enter to use default 80 for http): ")).strip()
    if port_input:
        try:
            port = int(port_input)
        except ValueError:
            print(color_red("Invalid port number. Using default http port."))
elif connection_type == '2':
    port = 443
    port_input = input(color_red("Enter target port (or press Enter to use default 443 for https): ")).strip()
    if port_input:
        try:
            port = int(port_input)
        except ValueError:
            print(color_red("Invalid port number. Using default port."))
else:
    print(color_red("Invalid connection type. Please choose '1' for http or '2' for https."))
    exit(1)

timeout = int(input(color_red("Enter the timeout in seconds: ")))

check_h2(url, port, timeout, connection_type)
