# @title
import random as random
import threading
from datetime import datetime
import numpy as np
import cProfile

casasDoTabuleiro = [0] * 41
lista_de_duplas_por_posicao = []
lista_de_rolagens = []
rolagem_das_posicoes = []
primeira_vez_na_cadeia = []
passos_ate_a_cadeia = []


def rolar_dado():
    dice_possibilities = [1, 2, 3, 4, 5, 6]
    return random.choice(dice_possibilities)


def percorrer_o_tabuleiro(turnos):
    duplas = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    posicao_atual = 0
    n_duplas = 0
    turnos_cadeia = 0
    esta_na_cadeia = False
    newLista = []
    lista_de_rolagens.append((0, (0, 0), -1, 'Primeira Jogada'))
    for i in range(turnos):
        primeiro_dado = rolar_dado()
        segundo_dado = rolar_dado()
        rolagem_dos_dados = primeiro_dado + segundo_dado
        if (primeiro_dado, segundo_dado) in duplas[0:7]:
            if esta_na_cadeia:
                # primeira_vez_na_cadeia.append(i + 1)
                n_duplas = 0
                esta_na_cadeia = False
                turnos_cadeia = 0
                # lista_de_rolagens.append((posicao_atual, (primeiro_dado, segundo_dado), i, 'Livre'))
                # newLista.append((posicao_atual, (primeiro_dado, segundo_dado), i, True, 'Livre'))
                # rolagem_das_posicoes.append((posicao_atual, i, 'Livre'))
            else:
                n_duplas += 1
                # lista_de_duplas_por_posicao.append((posicao_atual, n_duplas, i))
                # lista_de_rolagens.append((posicao_atual, (primeiro_dado, segundo_dado), i, 'Livre'))
                newLista.append((posicao_atual, (primeiro_dado, segundo_dado), i, True, 'Livre'))
                # rolagem_das_posicoes.append((posicao_atual, i, 'Livre'))
        else:
            if esta_na_cadeia:
                # primeira_vez_na_cadeia.append(i + 1)
                posicao_atual = (posicao_atual + rolagem_dos_dados) % 40
                # casasDoTabuleiro[posicao_atual] = casasDoTabuleiro[posicao_atual] + 1
                # lista_de_rolagens.append((posicao_atual, (primeiro_dado, segundo_dado), i, 'Cadeia'))
                break
                # rolagem_das_posicoes.append((posicao_atual, i, 'Cadeia'))
                n_duplas = 0
            else:
                posicao_atual = (posicao_atual + rolagem_dos_dados) % 40
                # casasDoTabuleiro[posicao_atual] = casasDoTabuleiro[posicao_atual] + 1
                # lista_de_rolagens.append((posicao_atual, (primeiro_dado, segundo_dado), i, 'Livre'))
                newLista.append((posicao_atual, (primeiro_dado, segundo_dado), i, False, 'Livre'))
                # rolagem_das_posicoes.append((posicao_atual, i, 'Livre'))
                n_duplas = 0
        if n_duplas == 3:
            esta_na_cadeia = True
            turnos_cadeia += 1
            casasDoTabuleiro[40] += 1
            newLista.append((posicao_atual, (primeiro_dado, segundo_dado), i, False, 'Cadeia'))
            break
        elif turnos_cadeia == 3:
            esta_na_cadeia = False
            n_duplas = 0
            turnos_cadeia = 0
    return newLista


def printar(casas):
    for cont, value in enumerate(casas):
        print(f'C[{cont}]:{value:5f}\t', end='\n')


def distribuicao_geometrica(probabilidade_cadeia, passos):
    return pow(1 - probabilidade_cadeia, passos - 1) * probabilidade_cadeia


turnos = 100000


# percorrer_o_tabuleiro(turnos)

def achar_passos_ate_a_cadeia(lista_de_rolagem):
    passos = []
    for i in range(len(lista_de_rolagem)):
        if not lista_de_rolagem[i][4] == 'Cadeia':
            if not lista_de_rolagem[i][3]:
                passos.append([i][0])
        else:
            break
        if len(passos) >= turnos:
            return 0
    return len(passos)


def simulacao(qtdSimulacoes):
    lista = []
    media_de_passos = 0
    for i in range(qtdSimulacoes):
        lista = percorrer_o_tabuleiro(turnos)
        passos = achar_passos_ate_a_cadeia(lista)
        media_de_passos += passos
        lista = []
    return media_de_passos / qtdSimulacoes


# print(simulacao(1000))

if __name__ == "__main__":
    print(simulacao(100000))

# printar(casasDoTabuleiro)
# printar([x / turnos for x in casasDoTabuleiro])

# print("\nCasas com duplas, numero de duplas, turno")
# for i in range(len(lista_de_duplas_por_posicao)):
#     print(f'Casa: {lista_de_duplas_por_posicao[i][0]}, '
#           f'Numero Duplas: {lista_de_duplas_por_posicao[i][1]}, '
#           f'Turno: {lista_de_duplas_por_posicao[i][2]}')
# #
# print("\nLista de rolagem, dados, turnos")
# for i in range(len(lista_de_rolagens)):
#     print(f'Casa: {lista_de_rolagens[i][0]}, '
#           f'Dados: {lista_de_rolagens[i][1]}, '
#           f'Turno: {lista_de_rolagens[i][2]}, '
#           f'Status: {lista_de_rolagens[i][3]}')
#
# print("\nPosicao Ao Longo dos Turnos")
# for i in range(len(rolagem_das_posicoes)):
#     print(f'Casa: {rolagem_das_posicoes[i][0]}, '
#           f'Turno: {rolagem_das_posicoes[i][1]}, '
#           f'Status: {rolagem_das_posicoes[i][2]}')
