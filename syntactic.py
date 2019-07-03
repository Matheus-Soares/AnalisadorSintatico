# -*- coding: utf-8 -*-
import csv
import sys
import os
import subprocess
import numpy as np
from stack import Stack
from symbol_table import SymbolTable

# Variaveis globais
rules = []
rules.append([""])

parser = {}

file = open("print_stacks.txt", "w")


def read_rules(path):
        # Le as regras da gramática e insere num vetor
        # Primeira posição nula para fechar com o numero de regras

    with open(path, "r") as rules_:
        for i, line in enumerate(rules_):
            rules.append(list(map(int, line.split())))


def read_parser(path):
        # Le a tabela de parsing e insere em um dicionario aninhado

    with open(path, "r") as table_:
        for line in table_:
            num = line.split()
            try:
                parser[int(num[0])][int(num[1])] = int(num[2])
            except:
                parser[int(num[0])] = {}
                parser[int(num[0])][int(num[1])] = int(num[2])


def read_input(path):
        # Le a entrada atraves da linha de comando
        # e insere em uma pilha

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


def init():
        # Inicia as variaveis
        # Le as regras e tabela de parsing
        # Le o arquivo de entrada e inicia pilha

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


def print_stacks(stack, input):
    file.write("\nPilha:")
    file.write(str(stack))

    file.write("\n\nEntrada:")
    file.write(str(input))
    file.write("\n\n---------------------\n")


def syntatic(stack, input):
        # Algoritmo descendente sem backtracking

    table = SymbolTable()

    X = stack.top()
    a = input.top()[1]
    lex = input.top()[0]
    callfuncao = False
    declarado = False
    function = False

    while X is not "$":

        print("X = {}\ta = {}\t lexema = {}".format(X, a, lex))

        # Se X é î (token de î = 17)
        if X == 17:
            ##
            # print('1')
            ##
            stack.pop()
            X = stack.top()

            # Incluindo alterações no arquivo
            file.write("--> X == 17 (Retirou elemento vazio da pilha)")
            print_stacks(stack, input)

        # Se X é terminal
        elif X <= 50:
            ##
            # print('2')
            ##
            if X == a:
                if a == 41 and declarado:
                    declarado = False

                # callfuncao
                if a == 27:
                    name = input.stack[-2][0]
                    callfuncao = True
                    if not table.search(name):
                        print("\nErro na linha {}: Função não declarada".format(
                            int(input.top()[2]) + 1))
                        exit()

                # Se for uma chamada de funçao
                if a == 7 and callfuncao:
                    function = True
                    params = []
                    if input.stack[-2][0] == '(':
                        i = -3
                        p = input.stack[i][0]
                        while p != ')':
                            if p != ',':
                                try:
                                    p = table.table[p]['type']
                                except:
                                    if input.stack[i][1] == 5:
                                        p = 'integer'
                                    if input.stack[i][1] == 6:
                                        p = 'float'
                                    if input.stack[i][1] == 8:
                                        p = 'char'
                                params.append(p)
                            i -= 1
                            p = input.stack[i][0]

                    if not params:
                        params = None

                    if params != table.table[name]['params']:
                        print("\nErro na linha {}: Parametros incorretos".format(
                            int(input.top()[2]) + 1))
                        exit()

                    callfuncao = False
                    stack.pop()
                    input.pop()
                    X = stack.top()
                    a = input.top()[1]
                    lex = input.top()[0]
                    continue

                # Atribuição
                if a == 7 and input.stack[-2][0] == '=':
                    if not table.search(input.top()[0]):
                        print("\nErro na linha {}: Variável não declarada.".format(
                            int(input.top()[2]) + 1))
                        exit()

                    type = input.stack[-3][1]

                    if type == 5:
                        if not (table.table[input.stack[-1][0]]['type'] == 'integer'):
                            print("\nErro na linha {}: Atribuição incorreta".format(
                                int(input.top()[2]) + 1))
                            exit()

                    elif type == 6:
                        if not (table.table[input.stack[-1][0]]['type'] == 'float'):
                            print("\nErro na linha {}: Atribuição incorreta".format(
                                int(input.top()[2]) + 1))
                            exit()

                    elif type == 8:
                        if not (table.table[input.stack[-1][0]]['type'] == 'char'):
                            print("\nErro na linha {}: Atribuição incorreta".format(
                                int(input.top()[2]) + 1))
                            exit()

                # Se for uma variavel
                if a == 7 and not declarado and not function:
                    if not table.search(input.top()[0]):
                        # Nome de função sem parametos
                        if input.stack[-2][0] == '{':
                            # Add (name, cat, type, level, params=None)
                            table.add(input.top()[0], 'f', 0, 0)

                        # Nome de função com parametros
                        elif input.stack[-2][0] == '(':
                            params = []
                            i = -3
                            p = input.stack[i][0]
                            while p != ')':
                                if p != ';':
                                    params.append(p)
                                i -= 1
                                p = input.stack[i][0]
                            # Add (name, cat, type, level, params=None)
                            table.add(input.top()[0], 'f', 0, 0, params=params)

                        # Declaração de uma variável
                        elif input.stack[-2][0] == ':':
                            type = input.stack[-3][0]
                            table.add(input.top()[0], 'v', type, 0)

                        # Declaração de mais de uma variável
                        elif input.stack[-2][0] == ',':
                            declarado = True
                            i = -3
                            variaveis = []
                            variaveis.append(input.top()[0])
                            p = input.stack[i][0]
                            while p != ':':
                                if p == ',':
                                    i -= 1
                                else:
                                    variaveis.append(p)
                                i -= 1
                                p = input.stack[i][0]

                            type = input.stack[i - 1][0]

                            for v in variaveis:
                                # Add (name, cat, type, level, params=None)
                                table.add(v, 'v', type, 0)
                        else:
                            print("\nErro na linha {}: Variável não declarada".format(
                                int(input.top()[2]) + 1))
                            exit()

                    else:
                        # Não está declarando variável
                        if input.stack[-2][0] != ',' or input.stack[-2][0] == ':':
                            stack.pop()
                            input.pop()
                            X = stack.top()
                            a = input.top()[1]
                            lex = input.top()[0]
                            continue
                        # Erro
                        print("\nErro na linha {}: Redeclaração de variáveis".format(
                            int(input.top()[2]) + 1))
                        table.print()
                        exit()

                stack.pop()
                input.pop()

                # Incluindo alterações no arquivo
                file.write(
                    "--> X == a (Retirou os elementos da pilha e da entrada)")
                print_stacks(stack, input)

                if input.top() == '$' and stack.top() == '$':
                    break

                X = stack.top()
                a = input.top()[1]
                lex = input.top()[0]
                continue
            else:
                ##
                # print('4')
                ##
                print("\nErro na linha {}".format(int(input.top()[2]) + 1))
                exit()
        # Se X é não teminal
        elif X > 50:
            ##
            # print('5')
            ##
            try:
                ##
                # print('6')
                ##
                r = parser[X][a]
                s = rules[r]
                stack.pop()

                for i in reversed(list(s)):
                    stack.push(i)
                X = stack.top()

                # Incluindo alterações no arquivo
                file.write("--> X > 50 (Incluiu regra {} na pilha)".format(r))
                print_stacks(stack, input)

                continue
            except:
                ##
                # print('7')
                ##
                #print("\nStack: {}".format(stack))
                #print("input: {}".format(input))
                print("\nErro na linha {}".format(int(input.top()[2]) + 1))
                exit()


if __name__ == "__main__":
        # Função principal

    if len(sys.argv) < 2:
        print("Execute com \n\t'python3 syntatic.py 'CodigoFonte.blocky'")
        exit()

    print("____Analisador Léxico____")
    subprocess.call(['python', 'lexico/lexical.py', sys.argv[1]])

    print("\n\n____Analisador Sintático____")

    stack, input = init()

    file.write("Pilas iniciais:\n")

    file.write("\nPilha:")
    file.write(str(stack))

    file.write("\n\nEntrada:")
    file.write(str(input))
    file.write("\n\n---------------------\n")

    syntatic(stack, input)

    print("\n\n____Código correto____")
    print("____Verifique arquivo 'print_stacks.txt' para maiores informações____")
