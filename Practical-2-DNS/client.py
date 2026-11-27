import socket


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


def main():
    print("DNS CLIENT APPLICATION")
    print("----------------------")

    while True:
        domain = input("\nEnter domain name (or 'exit' to quit): ").strip()

        if domain.lower() == "exit":
            print("Client application closed.")
            break

        if not domain:
            print("Please enter a valid domain name.")
            continue

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                client_socket.sendall((domain + "\n").encode("utf-8"))

                with client_socket.makefile("r", encoding="utf-8") as response_stream:
                    response = response_stream.readline().strip()

            print("\nServer Response:")
            print(response)
        except ConnectionRefusedError:
            print("ERROR: DNS server is not running.")
        except OSError as error:
            print(f"Network error: {error}")


if __name__ == "__main__":
    main()
