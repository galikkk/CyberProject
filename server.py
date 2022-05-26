import socket

# Initialize s to socket
s = socket.socket()

# Initialize the host
host = socket.gethostname()

# Initialize the port
port = 8080

# Bind the socket with port and host
s.bind(('', port))

print("waiting for connections...")

# listening for connections
s.listen()

# accepting the incoming connections
conn, addr = s.accept()

print(addr, "is connected to server")

while True:
	# take command as input
	command = input(str("Enter Command :"))

	conn.send(command.encode())

	print("Command has been sent successfully.")

	if command == "close":
		break

	# receive the confirmation
	data = conn.recv(32).decode()

	if data:
		print("command received and executed successfully.")
		print(data)