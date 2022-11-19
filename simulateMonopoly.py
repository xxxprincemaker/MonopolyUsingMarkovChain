#@title Letra A - Caso 3)
import numpy as np
import scipy.linalg as la
import math
import matplotlib.pyplot as plt
import scipy as sci
import csv
from fractions import Fraction

import scipy.sparse


def probabilidade_normal_sem_dupla():
    probability = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    probability[1:12:2] = np.subtract(probability[1:12:2], 1)
    probability = [x / 36 for x in probability]
    return probability


def probabilidade_de_rolar_apenas_duplas():
    probability = np.zeros(12)
    probability[1:12:2] = 1
    probability = [x / 36 for x in probability]
    return probability


def transforma_em_matrix_e_printa(matriz, x1Limitador=0, x2Limitador=123):
    x = '\n'.join(
        [f'\t'.join([f' {str(Fraction(item).limit_denominator()):<10}' for item in linha]) for contador, linha in
         enumerate(matriz) if (contador >= x1Limitador)
         and (contador <= x2Limitador)])
    print(x)


def criar_matrix(probs):
    m = np.zeros([40, 40])
    mm = np.zeros([40, 40])

    for i in range(40):
        for count, value in enumerate(probs):
            mm[i, (-40 + i + count + 1)] = value
    m[:40, :40] = mm

    return m


def corretude(m, nome):
    if nome == 'final':
        for i in range(42):
            s = np.sum(m[:, i])
            if s != 1:
                print(f'Probabilidade da soma de {s:.6f} na coluna {i} na matrix {nome}')
    else:
        for i in range(123):
            s = np.sum(m[i, :])
            if s != 1.0:
                print(f'Probabilidade da soma de {s:.6f} na linha {i} na matrix {nome}')


matrix_de_transicao = np.zeros([123, 123])

rolagem_normal = probabilidade_normal_sem_dupla()
rolagem_normal_matrix = criar_matrix(rolagem_normal)

rolagem_dupla = probabilidade_de_rolar_apenas_duplas()
rolagem_dupla_matrix = criar_matrix(rolagem_dupla)

# Regra das Duplas
matrix_de_transicao[0:40, 0:40] = rolagem_normal_matrix
matrix_de_transicao[0:40, 40:80] = rolagem_dupla_matrix

matrix_de_transicao[40:80, 0:40] = rolagem_normal_matrix
matrix_de_transicao[40:80, 80:120] = rolagem_dupla_matrix

matrix_de_transicao[80:120, 0:40] = rolagem_normal_matrix

matrix_de_transicao[80:120, 121] = 1 - np.sum(matrix_de_transicao[80:120, 0:120], 1)

# Ficar na cadeia

# Primeiro Turno
matrix_de_transicao[120, 0:40] = rolagem_dupla_matrix[20, :]
matrix_de_transicao[120, 121] = 1 - np.sum(matrix_de_transicao[120, 0:120])

# Segundo Turno
matrix_de_transicao[121, 0:40] = rolagem_dupla_matrix[20, :]
matrix_de_transicao[121, 122] = 1 - np.sum(matrix_de_transicao[121, 0:120])

#Terceiro Turno
matrix_de_transicao[122, 0:40] = rolagem_dupla_matrix[20, :] + rolagem_normal_matrix[20, :]

transforma_em_matrix_e_printa(matrix_de_transicao, 0, 124)
corretude(matrix_de_transicao, 'teste')

# Distribuição Estacionaria
ein_value, ein_vec = la.eig(matrix_de_transicao.conjugate().T)
distribuicao_estacionaria_vector = np.power(ein_vec[:, 0], 2)
distribuicao_estacionaria_vector[0:40] = distribuicao_estacionaria_vector[0:40] + distribuicao_estacionaria_vector[40:80] + distribuicao_estacionaria_vector[80:120]
distribuicao_estacionaria_vector[0:40] = distribuicao_estacionaria_vector[0:40]
distribuicao_estacionaria_vector[40] = np.sum(distribuicao_estacionaria_vector[120:123])
distribuicao_estacionaria_vector = distribuicao_estacionaria_vector[0:41].real
distribuicao_estacionaria_vector[20] += distribuicao_estacionaria_vector[40]

for counter, element in enumerate(distribuicao_estacionaria_vector):
    print(f'P(x={counter}): {element:.4f}')