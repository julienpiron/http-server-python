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
    if(not isinstance(url, str)):
        raise Exception("Invalid URL")

    if(url == "/"):
        client.send(b"HTTP/1.1 200 OK\r\n\r\n")
    if(url.startswith("/echo/")):
        payload = url[6:]
        client.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(payload)}\r\n\r\n{payload}".encode("utf-8"))
    else:
        client.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    client.close()


if __name__ == "__main__":
    main()
