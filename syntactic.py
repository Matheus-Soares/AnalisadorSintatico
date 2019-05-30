import csv
import sys
import os
import subprocess
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
		file = csv.reader(file_, delimiter='\t')

		# Inserindo em ordem reversa,
		# assim o primeiro token esta no topo da pilha
		for line in reversed(list(file)):
			if not line == "\n":
				line_ = [line[0], int(line[1]), int(line[2])]

				stack.push(line_)

	return stack

# Inicia as variaveis
# Le as regras e tabela de parsing 
# Le o arquivo de entrada e inicia pilha
def init():
	# Le as regras
	read_rules("files/rules.csv")

	# Le a tabela de parsing
	read_parser("files/table.csv")

	# Le o arquivo de entrada e coloca em uma pilha
	input_ = read_input('out.csv')
	
	# Inicia a pilha com o item inicial
	stack = Stack()
	stack.push("$")
	stack.push(51)

	return stack, input_

def syntatic(stack, input):
	#Algoritmo descendente sem backtracking
	X = stack.top()
	a = input.top()[1]
	tk = input.top()[0]

	while X is not "$":

		print("X = {}\ta = {}\t token = {}".format(X, a, tk))

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

				if input.top() == '$' and stack.top() == '$':
					break

				X = stack.top()
				a = input.top()[1]
				tk = input.top()[0]
				continue
			else:
				##
				#print('4')
				##
				print("\nErro na linha {}".format(int(input.top()[2]) + 1))
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
				continue
			except:
				##
				#print('7')
				##
				#print("\nStack: {}".format(stack))
				#print("input: {}".format(input))
				print("\nErro na linha {}".format(int(input.top()[2]) + 1))
				exit()



# Função principal
if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print("Execute com \n\t'python3 syntatic.py 'CodigoFonte.blocky'")
		exit()

	print("____Analisador Léxico____")
	subprocess.call(['python3', 'lexico/lexical.py', sys.argv[1]])
	

	print("\n\n____Analisador Sintático____")

	stack, input = init()

	syntatic(stack, input)

	print("\n\n____Código sintaticamente correto____")


