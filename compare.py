import random


def left_is_smaller(x, y, all_connections, closed_clients):
	# Cheating to make it easier to understand
	if x == y:
		return False

	# Chooses a random client to ask a question
	active_client = random.choice(all_connections)
	inactive_clients = []

	# List that includes all but the active client
	if len(all_connections) != 0:
		for item in all_connections:
			if item != active_client:
				inactive_clients.append(item)

	# Add a point to the active clients score
	active_client[4] += 1

	# Send a message to all the waiting clients
	for client in inactive_clients:
		client[0].sendall(("Waiting for " + str(active_client[3])).encode("utf-8"))

	# Ask the active client and receive an answer
	active_client[0].sendall((str(x) + " > " + str(y) + "  y/n ?\n").encode("utf-8"))
	data = active_client[0].recv(1024)
	data = data.decode("utf-8")

	# Remove the client without crashing the system
	if "exit" in data.lower():
		# Close the clients connection
		closed_clients.append(active_client)
		active_client[0].close()
		all_connections.remove(active_client)  # Remove the client from the list of clients

		# Asking the question to the new list of clients
		return left_is_smaller(x, y, all_connections, closed_clients)

	# Return the appropriate answer
	if "y" in data.lower():
		return False
	elif "n" in data.lower():
		return True

	# Ask again if no answer was found
	else:
		return left_is_smaller(x, y, all_connections, closed_clients)
