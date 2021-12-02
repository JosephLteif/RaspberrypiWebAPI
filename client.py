import socket
import time
import errno
import sys

class Client():
    def __init__(self, device_info):
        self.HEADER_LENGTH = 10
        self.IP = device_info["listening_ip"]
        self.PORT = device_info["listening_port"]
        self.name =  device_info["name"]
        self.delay = 0.1

    def connect(self):
        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        client_socket.connect((self.IP, self.PORT))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = self.name.encode('utf-8')
        username_header = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)

        loop = True
        while(loop):

            # here we put the sensor function here
            message = "hello"

            # If message is not empty - send it
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)

            try:
                while True:

                    # Receive our "header" containing message length, it's size is defined and constant
                    message_header = client_socket.recv(self.HEADER_LENGTH)

                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(message_header):
                        print('Connection closed by the server')
                        sys.exit()

                    message_length = int(message_header.decode('utf-8').strip())
                    message = client_socket.recv(message_length).decode('utf-8')

                    if(message == "stop"):
                        loop = False


            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()

                # We just did not receive anything
                continue

            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                sys.exit()
        time.sleep(self.delay)
