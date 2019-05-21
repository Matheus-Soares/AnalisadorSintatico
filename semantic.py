import csv
import sys

class Stack:
	def __init__(self):
		self.__stack = []

	def __len__(self):
		return len(self.__stack)

	def __repr__(self):
		l = print(self.__stack)
		return "<" + str(l) + ">"

	def __str__(self):
		return "Non implemented function"

	def is_empty(self):
		return len(self.__stack) == 0

	def push(self,element):
		self.__stack.append(element)

	def pop(self):
		if(self.is_empty()):
			raise(Empty('Stack is empty')) 
		else:
			return self.__stack.pop()

	def top(self):
		if(self.is_empty()):
			raise(Empty('Stack is empty'))
		else:
			return self.__stack[-1]   


def read_input():
	stack = Stack()

	# Lendo a arquivo de saída do analisador lexico
	with open(sys.argv[1], "r") as file_:
		file = csv.reader(file_, delimiter=',')

		# Inserindo em ordem reversa,
		# assim o primeiro token esta no topo da pilha
		for line in reversed(list(file)):
			if not line == "\n":
				stack.push(line)

	return stack

if __name__ == "__main__":

	istack = read_input()
	
	print(istack.pop())
