import socket
import re

PORT = 4221

requestLineRegex = re.compile(r"^(?P<method>GET) (?P<url>[^\s]*)")

def main():
    server_socket = socket.create_server(("localhost", PORT), reuse_port=True)
    print(f"Listening on port {PORT}")

    [client,_] = server_socket.accept() 

    req = client.recv(1024).decode()
    requestLine = requestLineRegex.match(req.splitlines()[0])
    if requestLine == None:
        return None
    url = requestLine.group("url")

    if(url == "/"):
        client.send(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        client.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    client.close()


if __name__ == "__main__":
    main()
