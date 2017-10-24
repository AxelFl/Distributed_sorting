import compare
import random

# All different sorting methods
# Not all of them work


def bubble(list, connn):
	for i in range(len(list) - 1, 0, -1):
		for b in range(0, i):
			if compare.left_is_smaller(list[b], list[b + 1], connn):
				pass
			else:
				list[b], list[b + 1] = list[b + 1], list[b]
	return list


def swapping(tosort, start, conn):
	for i in range(start, len(tosort) - 1, 2):
		if compare.left_is_smaller(tosort[i], tosort[i + 1], conn):
			tosort[i], tosort[i + 1] = tosort[i + 1], tosort[i]
			listret = [tosort, False]
			return listret
		else:
			listret = [tosort, True]
			return listret
	return


def oddEven(x, conn):
	is_sorted = False
	con = random.choice(conn)
	while not is_sorted:
		is_sorted = True
		for i in range(0, len(x)-1, 2):
			if compare.left_is_smaller(x[i+1], x[i], con[0]):
				x[i], x[i+1] = x[i+1], x[i]
				is_sorted = False
		for i in range(1, len(x)-1, 2):
			if compare.left_is_smaller(x[i+1], x[i], con[0]):
				x[i], x[i+1] = x[i+1], x[i]
				is_sorted = False
	return x


def quick(list, conn):
	if len(list) <= 1:
		return list
	list1 = []
	list2 = []
	pivot = random.choice(list)
	for number in list:
		if compare.left_is_smaller(pivot, number, conn):
			list2.append(number)
		else:
			list1.append(number)
	return quick(list1, conn) + quick(list2, conn)


def semiQuick(list ,conn):
	if len(list) <= 1:
		return list
	if len(list) <= 3:
		return bubble(list, conn)
	list1 = []
	list2 = []
	pivot = random.choice(list)
	for number in list:
		if compare.left_is_smaller(pivot, number, conn):
			list2.append(number)
		else:
			list1.append(number)
	return semiQuick(list1, conn) + semiQuick(list2, conn)

