import socket
from threading import Thread

import cv2
import datetime


def receive():
    command = s.recv(8)
    command = command.decode().lower()
    if command == 'stop':
        global flag
        flag = False
    #elif command == 'close':
     #   global flag1
      #  flag1 = False
    else:
        s.send("Command error".encode())


flag1 = True
# Initialize s to socket
s = socket.socket()

# Initialize the host
host = "127.0.0.1"

# Initialize the port
port = 8080

# bind the socket with port and host
s.connect((host, port))

print("Connected to Server.")

while True:
    # receive the command from master program
    command = s.recv(8)
    command = command.decode().lower()

    # match the command and execute it on slave system
    if command == "open":
        flag = True
        print("Command is :", command)
        s.send("Command received".encode())

        # open camera
        time = datetime.datetime.now()
        time = str(time)
        time = time.replace(":", ".")
        out_path = './' + time + '.mp4'
        print(out_path)

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

        while flag:
            ret, frame = cap.read()
            cv2.imshow('Input', frame)
            out.write(frame)

            c = cv2.waitKey(1)

            #if c == ord(' '):
             #   break

        s.send("Command recieved".encode())
        out.release()
        cap.release()
        cv2.destroyAllWindows()

    elif command == "close":
        break

    else:
        s.send("Command error".encode())
