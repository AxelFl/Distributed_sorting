import socket
import sorting_algorithm
import random
import time


# Returns IP address
def get_ip_address():
	ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip_socket.connect(("8.8.8.8", 80))
	return ip_socket.getsockname()[0]


HOST = ''  # Symbolic name, meaning all available interfaces
host = str(get_ip_address())
port = 2000
connections = []
inactive_connections = []
found_port = False
list_length = 5

# Initialize the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Go though the ports and grab the first available one
while not found_port:
	try:
		s.bind((host, port))
		found_port = True
	except OSError:
		# Try to grab the next port
		port += 1

# Announce the IP and Port to the terminal
print("On ip", get_ip_address())
print("On port", port)

# The first connection outside of the loop to avoid issues with server having no clients
s.listen(2)
newClient, newAddr = s.accept()
connections.append([newClient, newAddr, 0, "", 0])
connections[len(connections) - 1][0].sendall("What is your name?\n".encode("utf-8"))
connections[len(connections) - 1][3] = (connections[len(connections) - 1][0].recv(1024)).decode("utf-8")

s.settimeout(0.5)

# Allows multiple clients to connect at the start
time.sleep(2)

# Main loop
while True:

	# Try to add all clients until there are no new ones
	# Connects clients att the start of every sorting loop
	try:
		while 1:
			newClient, newAddr = s.accept()
			connections.append([newClient, newAddr, 0, "", 0])
			connections[len(connections) - 1][0].sendall("What is your name?\n".encode("utf-8"))
			connections[len(connections) - 1][3] = (connections[len(connections) - 1][0].recv(1024)).decode("utf-8")

			for inactive in inactive_connections:
				if inactive[3] == connections[len(connections) - 1][3]:
					connections[len(connections) - 1][2] = inactive[2]
					connections[len(connections) - 1][4] = inactive[4]
					inactive_connections.remove(inactive)
			time.sleep(0.2)
	except socket.timeout:  # No new clients
		pass

	# "Try" to exit the server if someone leaves by closing the connection themselves
	try:
		inputList = list(range(1, list_length + 1))
		random.shuffle(inputList)
		print("Random list:", inputList)

		# Randomize what sorting algorithm gets used
		random_number = random.randint(0, 2)

		# Start a sorting method and send the result
		if random_number == 0:
			inputList = sorting_algorithm.quick(inputList, connections, inactive_connections)
			print("Random list:", inputList)
			if all(inputList[i] <= inputList[i + 1] for i in range(len(inputList) - 1)):
				for client in connections:
					client[2] += client[4]
			for client in connections:
					client[4] = 0

			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using Quick sort: " + str(inputList) + "\nYou have " + str(
						connection[2]) + " points!\n").encode("utf-8"))

		if random_number == 1:
			inputList = sorting_algorithm.bubble(inputList, connections, inactive_connections)
			print("Sorted list:", inputList)
			if all(inputList[i] <= inputList[i + 1] for i in range(len(inputList) - 1)):
				for client in connections:
					client[2] += client[4]
			for client in connections:
				client[4] = 0

			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using Bubble sort: " + str(inputList) + "\nYou have " + str(
						connection[2]) + " points!\n").encode("utf-8"))

		if random_number == 2:
			inputList = sorting_algorithm.semiQuick(inputList, connections, inactive_connections)
			print("Sorted list:", inputList)
			if all(inputList[i] <= inputList[i + 1] for i in range(len(inputList) - 1)):
				for client in connections:
					client[2] += client[4]
			for client in connections:
				client[4] = 0

			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using semiQuick sort: " + str(inputList) + "\nYou have " + str(
						connection[2]) + " points!\n").encode("utf-8"))

	except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError,
	        ConnectionResetError, OSError, IndexError, KeyboardInterrupt):
		print("Broken Connection")
		for b in connections:
			b[0].close()
		quit()
