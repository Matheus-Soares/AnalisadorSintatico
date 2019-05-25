import csv
import sys
import numpy as np
from stack import Stack 

# Variaveis globais
rules = []
rules.append([""])

parser = {}

# Le as regras da gramática e insere num vetor
# Primeira posição nula para fechar com o numero de regras
def read_rules(path):
	with open(path, "r") as rules_:
		for i, line in enumerate(rules_):
			rules.append(list(map(int, line.split())))


# Le a tabela de parsing e insere em um dicionario aninhado 
def read_parser(path):
	with open(path, "r") as table_:
		for line in table_:
			num = line.split()
			try:
				parser[int(num[0])][int(num[1])] = int(num[2]) 
			except:
				parser[int(num[0])] = {}
				parser[int(num[0])][int(num[1])] = int(num[2])

# Le a entrada atraves da linha de comando 
# e insere em uma pilha
def read_input(path):
	stack = Stack()
	stack.push("$")

	# Lendo a arquivo de saída do analisador lexico
	with open(path, "r") as file_:
		file = csv.reader(file_, delimiter=',')

		# Inserindo em ordem reversa,
		# assim o primeiro token esta no topo da pilha
		for line in reversed(list(file)):
			if not line == "\n":
				stack.push(list(map(int, line)))

	return stack

# Inicia as variaveis
# Le as regras e tabela de parsing 
# Le o arquivo de entrada e inicia pilha
def init():
	# Le as regras
	read_rules("rules.csv")

	# Le a tabela de parsing
	read_parser("table.csv")

	# Le o arquivo de entrada e coloca em uma pilha
	input_ = read_input(sys.argv[1])
	
	# Inicia a pilha com o item inicial
	stack = Stack()
	stack.push("$")
	stack.push(51)

	return stack, input_

def semantic(stack, input):
	#Algoriitmo do professor
	X = stack.top()
	a = input.top()[0]

	while X is not "$":

		print("X = {}\ta = {}".format(X, a))

		# Se X é î (token de î = 17)
		if X == 17:
			##
			#print('1')
			##
			stack.pop()
			X = stack.top()
		# Se X é terminal
		elif X <= 50:
			##
			#print('2')
			##
			if X == a:
				##
				#print('3')
				##
				stack.pop()
				input.pop()
				a = input.top()[0]
				X = stack.top()
				continue
			else:
				##
				#print('4')
				##
				print("Erro na linha {}".format(input.top()[1]))
				exit()
		# Se X é não teminal
		elif X > 50:
			##
			#print('5')
			##
			try:
				##
				#print('6')
				##
				s = rules[parser[X][a]]
				stack.pop()

				for i in reversed(list(s)):
					stack.push(i)
				X = stack.top()
			except:
				##
				#print('7')
				##
				print("\nStack: {}".format(stack))
				print("input: {}".format(input))
				print("\nErro na linha {}".format(input.top()[1]))
				exit()



# Função principal
if __name__ == "__main__":
	stack, input = init()

	semantic(stack, input)

