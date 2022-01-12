import socket
import os
import cv2
import datetime

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
    command = s.recv(1024)
    command = command.decode()

    # match the command and execute it on slave system
    if command == "open":
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
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, size)

        while True:
            ret, frame = cap.read()
            cv2.imshow('Input', frame)
            out.write(frame)

            c = cv2.waitKey(1)

            if c == ord(' '):
                break

        out.release()
        cap.release()
        cv2.destroyAllWindows()

    else:
        s.send("Command error".encode())

    # you can give batch file as input here
    os.system('dir')