import random


def left_is_smaller(x, y, conn):
    if x == y:
        return False
    con = random.choice(conn)
    temp = []
    if len(conn) != 0:
        for item in conn:
            if item != con:
                temp.append(item)
    for client in temp:
        client[0].sendall("Waiting...\n".encode("utf-8"))
    con[0].sendall((str(x) + " > " + str(y) + "  y/n ?\n").encode("utf-8"))
    data = con[0].recv(1024)
    data = data.decode("utf-8")
    if "y" in data.lower():
        return False
    elif "n" in data.lower():
        return True
    else:
        return left_is_smaller(x, y, conn)
