# -*- coding: utf-8 -*-

import csv
import sys

tokens = {}

# Palavras reservadas
espec = ["while", "void", "string", "return", "main", "integer", "inicio", "if",
         "for", "float", "fim", "else", "double", "do", "cout", "cin", "char", "callfuncao"]

# Simbolos
simbols = ["!", ">>", ">=", ">", "==", "=", "<=", "<<", "<", "++", "+",
           "}", "{", ";", ":", "/", ",", "*", ")", "(", "$", "!=", "--", "-"]

outputFile = open("out.csv", "w")

# Leitura da tabela de tokens


def read_tokens():
    with open("lexico/tokens.csv") as table_:
        table = csv.reader(table_, delimiter='\t')
        for row in table:
            tokens[row[0]] = row[1]


# Imprime tokens
def print_token(lex, row, type):
    # Normal lex
    if type == 0:
        print("<{}, {}, {}>" .format(lex, tokens[lex], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens[lex]) + "\t" + str(row) + "\n")

    # Numero float
    elif type == 1:
        print("<{}, {}, {}>" .format(lex, tokens["numerofloat"], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens["numerofloat"]) + "\t" + str(row) + "\n")

    # Numero inteiro
    elif type == 2:
        print("<{}, {}, {}>" .format(lex, tokens["numerointeiro"], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens["numerointeiro"]) + "\t" + str(row) + "\n")

    # literal
    elif type == 3:
        print("<{}, {}, {}>" .format(lex, tokens["literal"], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens["literal"]) + "\t" + str(row) + "\n")

    # nomevariavel
    elif type == 4:
        print("<{}, {}, {}>" .format(lex, tokens["nomevariavel"], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens["nomevariavel"]) + "\t" + str(row) + "\n")

    # nomevariavel
    elif type == 5:
        print("<{}, {}, {}>" .format(lex, tokens["nomedastring"], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens["nomedastring"]) + "\t" + str(row) + "\n")

    # nomedochar
    elif type == 6:
        print("<{}, {}, {}>" .format(lex, tokens["nomedochar"], row))
        outputFile.write(str(lex) + "\t" +
                         str(tokens["nomedochar"]) + "\t" + str(row) + "\n")


# Le arquivo e classifica lexicamente, indicando erros
def analyzer():
    print("<Lexema, Token, Linha, Atributo>\n")
    lex = ""
    row = 0
    count = 0

    with open(sys.argv[1], 'r') as code:

        # Sempre começa o while com um novo caracter nao reconhecido
        char = code.read(1)
        while char:
            lex = ""

            # Ignora espaços em branco
            if char == " " or char == "\t":
                char = code.read(1)
                continue

            # Incrementa linha
            elif char == "\n":
                row += 1
                char = code.read(1)
                continue

            # Comantarios
            elif char == "%":
                char = code.read(1)

                # Comentario em linha
                if char != "*":
                    char = code.read(1)
                    while char != "\n" and char:
                        char = code.read(1)
                    row += 1
                    char = code.read(1)
                    continue

                # Comentario em bloco
                else:
                    char1 = code.read(1)
                    char2 = code.read(1)
                    if char1 == "\n":
                        row += 1
                    while char1 != "*" and char2 != "%":
                        if char2 == "\n":
                            row += 1

                        char1 = char2
                        char2 = code.read(1)
                        if not char1 and not char2:
                            print(
                                "\tErro: Não foi fechado comentario em bloco. Linha {}." .format(row))
                            exit()

                    char = code.read(1)
                    continue

            # Se não for comentario
            else:
                # Se for digito
                if char.isdigit():
                    while char.isdigit() and char:
                        lex += char
                        char = code.read(1)

                    # Numero float
                    if char == ".":
                        char = code.read(1)

                        while char.isdigit() and char:
                            lex += char
                            char = code.read(1)

                        if not char or char == " " or char == "\n" or char == "\t":
                            # Numero float
                            print_token(lex, row, 1)

                            if char == "\n":
                                row += 1

                            char = code.read(1)
                            continue

                        elif char in simbols:
                            print_token(lex, row, 1)
                            continue

                        else:
                            print(
                                "\tErro: Caracter invalido. Linha {}." .format(row))
                            exit()

                    # Numero inteiro
                    else:
                        if not char or char == " " or char == "\n" or char == "\t":
                            print_token(lex, row, 2)

                            if char == "\n":
                                row += 1

                            char = code.read(1)
                            continue

                        elif char in simbols:
                            print_token(lex, row, 2)
                            continue
                        else:
                            print(
                                "\tErro: Caracter invalido. Linha {}." .format(row))
                            exit()

                else:
                    # Simbolos
                    if char in simbols:
                        lex += char
                        char2 = code.read(1)
                        lex += char2

                        if lex in simbols:
                            print_token(lex, row, 0)
                            char = code.read(1)
                            continue

                        else:
                            print_token(char, row, 0)
                            char = char2
                            continue

                    # Literal
                    elif char == "@":
                        count += 1
                        char = code.read(1)
                        while char != "@" and char:
                            lex += char
                            count += 1

                            # Tamanho maximo de 32 caracteres
                            if count > 32:
                                print(
                                    "\tErro: Excedido o tamanho maximo de literal. Linha {}." .format(row))
                                exit()

                            if char == "\n":
                                row += 1

                            char = code.read(1)

                        if not char:
                            print(
                                "\tErro: Não foi fechado literal. Linha {}." .format(row))
                            exit()

                        else:
                            count = 0
                            print_token(lex, row, 3)
                            char = code.read(1)
                            continue

                    # Outros casos: palavra reservada válida ou nome de
                    # variavel
                    else:
                        while char.isalnum() and char:
                            count += 1

                            # Tamanho maximo de 32 caracteres
                            if count > 32:
                                print(
                                    "\tErro: Excedido o tamanho maximo de nome de variavel. Linha {}." .format(row))
                                exit()
                            lex += char
                            char = code.read(1)

                        if char in simbols or char == " " or char == "\t" or char == "\n":
                            if lex in tokens:
                                print_token(lex, row, 0)
                            else:
                                print_token(lex, row, 4)

                            if char == "\n":
                                row += 1
                                char = code.read(1)
                            count = 0
                            continue

                        else:
                            if char == '"':
                                char = code.read(1)
                                while char != '"' and char:
                                    lex += char
                                    char = code.read(1)
                                if not char:
                                    print(
                                        "\tErro: Não foi fechado string. Linha {}." .format(row))
                                    exit()
                                else:
                                    if char == "\n":
                                        row += 1
                                    print_token(lex, row, 5)
                                    char = code.read(1)
                                    continue

                            if char == "'":
                                char = code.read(1)
                                lex += char
                                char1 = code.read(1)
                                if char1 == "'" and char and char1:
                                    print_token(lex, row, 6)
                                    char = code.read(1)
                                    continue
                                else:
                                    print(
                                        "\tErro: Declaração incorreta de char. Linha {}." .format(row))
                                    exit()

                            print(
                                "\tErro: Caracter invalido. Linha {}." .format(row))
                            exit()

    return()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: \n\tpython3 lexical.py 'your_file'.blocky")
    else:
        # Le a tabela de tokens
        read_tokens()

        # Le o arquivo passado como argumento e analisa lexicamente
        analyzer()
