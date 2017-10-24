import socket
import sorting_algorithm
import random
import time


def get_ip_address():
	ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip_socket.connect(("8.8.8.8", 80))
	return ip_socket.getsockname()[0]


HOST = ''  # Symbolic name, meaning all available interfaces
host = str(get_ip_address())
port = 2000
connections = []
works = False
list_length = 5

# Initialize the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Go though the ports and grab the first available one
while not works:
	try:
		s.bind((host, port))
		works = True
	except OSError:
		port += 1

# Announce the IP and Port to the terminal
print("On ip", get_ip_address())
print("On port", port)

# The first connection outside of the loop to avoid issues with no clients
s.listen(1)
newClient, newAddr = s.accept()
connections.append([newClient, newAddr, 0, ""])
connections[len(connections) - 1][0].sendall("What is your name?\n".encode("utf-8"))
connections[len(connections) - 1][3] = (connections[len(connections) - 1][0].recv(1024)).decode("utf-8")
s.settimeout(0.5)

time.sleep(2)

while True:

	# Try to add all clients until there are no new ones
	# Connects clients att the start of every sorting loop
	try:
		while 1:
			newClient, newAddr = s.accept()
			connections.append([newClient, newAddr, 0, ""])
			connections[len(connections) - 1][0].sendall("What is your name?\n".encode("utf-8"))
			connections[len(connections) - 1][3] = (connections[len(connections) - 1][0].recv(1024)).decode("utf-8")
			time.sleep(0.2)
	except socket.timeout: # No new clients
		pass

	try:
		inputList = list(range(1, list_length + 1))
		random.shuffle(inputList)
		print("Random list:", inputList, "\n")

		# Randomize what sorting algorithm gets used
		random_number = random.randint(0, 2)

		# Start a sorting method and send the result
		if random_number == 0:
			inputList = sorting_algorithm.quick(inputList, connections)
			print("Random list:", inputList)
			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using Quick sort: " + str(inputList) + "\nYou have " + str(connection[2]) + " points!\n").encode("utf-8"))
		if random_number == 1:
			inputList = sorting_algorithm.bubble(inputList, connections)
			print("Sorted list:", inputList)
			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using Bubble sort: " + str(inputList) + "\nYou have " + str(connection[2]) + " points!\n").encode("utf-8"))
		if random_number == 2:
			inputList = sorting_algorithm.semiQuick(inputList, connections)
			print("Sorted list:", inputList)
			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using semiQuick sort: " + str(inputList) + "\nYou have " + str(connection[2]) + " points!\n").encode("utf-8"))
	except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, ConnectionResetError, OSError):
		print("Broken Connection")
		for b in connections:
			b[0].close()
		quit()
