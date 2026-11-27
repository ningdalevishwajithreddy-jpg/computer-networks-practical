import socket


HOST = "127.0.0.1"
PORT = 5000


def resolve_domain(domain):
    try:
        _, _, ip_addresses = socket.gethostbyname_ex(domain)
        if ip_addresses:
            return f"SUCCESS: {domain} resolved to {', '.join(ip_addresses)}"
        return f"ERROR: No IPv4 address found for {domain}"
    except socket.gaierror:
        return f"ERROR: Unable to resolve domain {domain}"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print("DNS Server started successfully.", flush=True)
        print(f"Server listening on {HOST}:{PORT}", flush=True)

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    print(f"\nConnected to client: {client_address}", flush=True)

                    with client_socket.makefile("r", encoding="utf-8") as input_stream:
                        domain = input_stream.readline().strip()

                    if not domain:
                        continue

                    print(f"Received domain query: {domain}", flush=True)
                    result = resolve_domain(domain)
                    client_socket.sendall((result + "\n").encode("utf-8"))
                    print(f"Response sent: {result}", flush=True)
        except KeyboardInterrupt:
            print("\nDNS Server stopped.", flush=True)


if __name__ == "__main__":
    main()
