import socket
from threading import Thread

import cv2
import datetime

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Socket:
    def __init__(self, host, port):
        # Initialize the host and port
        self.__host = host
        self.__port = port
        self.__s = socket.SocketKind.SOCK_STREAM

    # make a connection between the client and the server
    def connect(self):
        #try:
            # Initialize s to socket
            self.__s = socket.socket()
            # bind the socket with port and host
            self.__s.connect((self.__host, self.__port))
            print("Connected to Server.")
        #except Exception as e:
         #   print(e)

    # receive message from the server
    def receive(self):
        command = self.__s.recv(8)
        command = command.decode().lower()
        return command

    # send message to the server
    def send(self, message):
        self.__s.send(message.encode())

    # close the connection
    def close(self):
        self.__s.close()


# receive message from the server
def receive():
    flag1 = True
    while flag1:
        command = s.receive()
        if command == 'stop':
            global flag
            flag = False
            flag1 = False
        else:
            s.send("Command error")


# returns the file name included the current date and time
def get_file_name():
    time = datetime.datetime.now()
    time = str(time)
    time = time.replace(":", ".")
    out_path = './' + time + '.mp4'
    print(out_path)
    return out_path


# upload the video file to Google Drive using Drive API
def upload_video_to_drive(out_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    upload_file_list = [out_path.strip("./")]
    for upload_file in upload_file_list:
        gfile = drive.CreateFile({'parents': [{'id': '1fvB8jlZ855MHywhuZOkSjIsehEcFMyFQ'}]})
        # Read file and set it as the content of this instance.
        gfile.SetContentFile(upload_file)
        gfile.Upload()  # Upload the file.

    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format('1fvB8jlZ855MHywhuZOkSjIsehEcFMyFQ')}).GetList()
    for file in file_list:
        print('title: %s, id: %s' % (file['title'], file['id']))

    s.send("video uploaded")


def main():
    while True:
        # receive the command from the server
        command = s.receive()
        # match the command and execute it on client system
        if command == "open":
            print("Command is :", command)
            s.send("Command received")

            # open camera
            out_path = get_file_name()

            cap = cv2.VideoCapture(0)

            # Check if the webcam is opened correctly
            if not cap.isOpened():
                raise IOError("Cannot open webcam")

            ret, frame = cap.read()
            height, width, layers = frame.shape
            size = width, height
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

            thread = Thread(target=receive)
            thread.start()

            # save the frames to one video file
            while flag:
                ret, frame = cap.read()
                cv2.imshow('Input', frame)
                out.write(frame)

                c = cv2.waitKey(1)

            s.send("Command received")
            out.release()
            cap.release()
            cv2.destroyAllWindows()

            break

        else:
            s.send("Command error")

    upload_video_to_drive(out_path)
    s.close()
    print("connection closed")


flag = True
try:
    # Initialize the host and port, connect to the server
    s = Socket("127.0.0.1", 8080)
    s.connect()

    if __name__ == "__main__":
        main()

except Exception as e:
    print(e)


