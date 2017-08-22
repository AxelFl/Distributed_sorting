import socket
import sorting_algorithm
import random

import time

HOST = ''  # Symbolic name, meaning all available interfaces
host = "172.16.1.183"
port = 2000
connections = []
works = False
notsorted_length = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while not works:
	try:
		s.bind((host, port))
		works = True
	except OSError:
		port += 1
print("On port", port)

s.listen(1)
newClient, newAddr = s.accept()
connections.append([newClient, newAddr, False])

s.settimeout(0.5)

while True:

	try:
		while 1:
			newClient, newAddr = s.accept()
			connections.append([newClient, newAddr, False])
			time.sleep(0.2)
	except socket.timeout:
		pass

	try:
		inputList = list(range(1, notsorted_length + 1))
		random.shuffle(inputList)
		print("Random list:", inputList, "\n")
		randomnumber = random.randint(0, 2)
		if randomnumber == 0:
			inputList = sorting_algorithm.quick(inputList, connections)
			print("Random list:", inputList)
			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using Quick sort: " + str(inputList) + "\n").encode("utf-8"))
		if randomnumber == 1:
			inputList = sorting_algorithm.bubble(inputList, connections)
			print("Sorted list:", inputList)
			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using Bubble sort: " + str(inputList) + "\n").encode("utf-8"))
		if randomnumber == 2:
			inputList = sorting_algorithm.semiQuick(inputList, connections)
			print("Sorted list:", inputList)
			for connection in connections:
				connection[0].sendall(
					("Done!\nFinished list using semiQuick sort: " + str(inputList) + "\n").encode("utf-8"))
	except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, ConnectionResetError, OSError):
		print("Broken Connection")
		for b in connections:
			b[0].close()
		quit()
