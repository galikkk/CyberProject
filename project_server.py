import socket
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Socket:
    def __init__(self, host, port):
        # # Initialize the host and port
        self.__host = host
        self.__port = port
        self.__s = socket.SocketKind.SOCK_STREAM
        self.__conn = socket.SocketKind.SOCK_STREAM

    def connect(self):
        # Initialize s to socket
        self.__s = socket.socket()
        # Bind the socket with port and host
        self.__s.bind(('', self.__port))
        print("waiting for connections...")
        # listening for connections
        self.__s.listen()
        # accepting the incoming connections
        self.__conn, addr = self.__s.accept()
        print(addr, "is connected to server")

    def send(self, command):
        self.__conn.send(command.encode())
        print("Command has been sent successfully.")

    def receive(self):
        data = self.__conn.recv(32).decode()
        return data

    def close(self):
        self.__s.close()


def download_video_from_drive():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format('1fvB8jlZ855MHywhuZOkSjIsehEcFMyFQ')}).GetList()

    for i, file in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
        print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
        file.GetContentFile(file['title'])


def main():
    s = Socket(socket.gethostname(), 8080)
    s.connect()

    while True:
        # take command as input
        command = input(str("Enter Command :"))
        s.send(command)
        if command == "stop":
            break

        data = s.receive()
        if data:
            print(data)

    data = s.receive()
    while data != "video uploaded":
        if data:
            print(data)
        data = s.receive()

    if data == "video uploaded":
        download_video_from_drive()

    s.close()
    print("connection closed")


if __name__ == "__main__":
    main()
