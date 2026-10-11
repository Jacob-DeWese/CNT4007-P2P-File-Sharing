import socket
import sys

class Client:
    def __init__(self,host="localhost",port=8000):
        self.host = host
        self.port = port
        self.requestSocket = None  # Socket connect to server
        self.out = None            # Stream write to the socket
        self.in_stream = None      # Stream read from the socket
        self.message = ""          # Message send to the server
        self.MESSAGE = ""          # Capitalized message read from the server

    def run(self):
        try:
            # Create a socket to connect to the server
            self.requestSocket = socket.create_connection((self.host, self.port))
            print(f"Connected to {self.host} in port {self.port}")

            # Initialize inputStream and outputStream
            self.out = self.requestSocket.makefile("w", encoding="utf-8")
            self.in_stream = self.requestSocket.makefile("r", encoding="utf-8")

            while True:
                # Read a sentence from the standard input
                self.message = input("Hello, please input a sentence: ")
                # Send the sentence to the server
                self.send_message(self.message)
                # Receive the upperCase sentence from the server
                self.MESSAGE = self.in_stream.readline()
                if not self.MESSAGE:
                    print("Server closed the connection")
                    break
                # Show the message to the user
                print("Receive message: " + self.MESSAGE)

        except ConnectionRefusedError:
            print("Connection refused. You need to initiate a server first.", file=sys.stderr)
        except socket.gaierror:
            print("You are trying to connect to an unknown host.", file=sys.stderr)
        except (EOFError, KeyboardInterrupt):
            print()
        except OSError as e:
            print(f"I/O error: {e}", file=sys.stderr)
        finally:
            # Close connection
            for stream in (self.in_stream, self.out, self.requestSocket):
                try:
                    if stream is not None:
                        stream.close()
                except OSError as e:
                    print(f"I/O error: {e}", file=sys.stderr)

    # Send a message to the output stream
    def send_message(self,message):
        try:
            # Stream write the message
            self.out.write(message + "\n")
            self.out.flush()
        except OSError as e:
            print(f"I/O error: {e}", file=sys.stderr)


# Main method
if __name__ == "__main__":
    client = Client()
    client.run()