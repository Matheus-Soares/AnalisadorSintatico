class Stack:

    def __init__(self):
        self.stack = []

    def __len__(self):
        return len(self.stack)

    def __repr__(self):
        l = print(self.stack)
        return "<" + str(l) + ">"

    def __str__(self):
        return str(self.stack)

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        if(self.is_empty()):
            raise(Empty('Stack is empty'))
        else:
            return self.stack.pop()

    def top(self):
        if(self.is_empty()):
            raise(Empty('Stack is empty'))
        else:
            return self.stack[-1]
