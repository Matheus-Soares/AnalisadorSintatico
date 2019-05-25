class Stack:
	def __init__(self):
		self.__stack = []

	def __len__(self):
		return len(self.__stack)

	def __repr__(self):
		l = print(self.__stack)
		return "<" + str(l) + ">"

	def __str__(self):
		return str(self.__stack)

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
