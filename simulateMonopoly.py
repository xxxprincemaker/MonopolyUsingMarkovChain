import numpy as np
import scipy.linalg as la
import math
import matplotlib.pyplot as plt
import scipy as sci
import csv
from fractions import Fraction

import scipy.sparse


def roll_probs():
    probability = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    probability[1:12:2] = np.subtract(probability[1:12:2], 1)
    probability = [x / 36 for x in probability]
    return probability


def roll_probs_double():
    probability = np.zeros(12)
    probability[1:12:2] = 1
    probability = [x / 36 for x in probability]
    return probability


def transformaEmFracaoEPrintar(matriz, x1Limitador=0, x2Limitador=123):
    x = '\n'.join(
        [f'\t'.join([f' {str(Fraction(item).limit_denominator()):<10}' for item in linha]) for contador, linha in
         enumerate(matriz) if (contador >= x1Limitador)
         or (contador <= x2Limitador)])
    print(x)


def create_matrix(probs):
    m = np.zeros([40, 40])
    mm = np.zeros([40, 40])

    for i in range(40):
        for count, value in enumerate(probs):
            mm[i, (-40 + i + count + 1)] = value
    m[:40, :40] = mm

    return m


def corretude(m, name):
    if name == 'steady':
        for i in range(42):
            s = np.sum(m[:, i])
            if s != 1:
                print(f'Probabilidade da soma de {s:.6f} na coluna {i} na matrix {name}')
    else:
        for i in range(123):
            s = np.sum(m[i, :])
            if s != 1.0:
                print(f'Probabilidade da soma de {s:.6f} na linha {i} na matrix {name}')


transition_matrix = np.zeros([123, 123])

ordinary_roll = roll_probs()
ordinary_roll_matrix = create_matrix(ordinary_roll)

double_roll = roll_probs_double()
double_roll_matrix = create_matrix(double_roll)

# Double Rule
transition_matrix[0:40, 0:40] = ordinary_roll_matrix
transition_matrix[0:40, 40:80] = double_roll_matrix

transition_matrix[40:80, 0:40] = ordinary_roll_matrix
transition_matrix[40:80, 80:120] = double_roll_matrix

transition_matrix[80:120, 0:40] = ordinary_roll_matrix

transition_matrix[80:120, 121] = 1 - np.sum(transition_matrix[80:120, 0:120], 1)

# Stay in the jail.
# 1st turn
transition_matrix[120, 0:40] = double_roll_matrix[20, :]
transition_matrix[120, 121] = 1 - np.sum(transition_matrix[120, 0:120])

# 2nd turn
transition_matrix[121, 0:40] = double_roll_matrix[20, :]
transition_matrix[121, 122] = 1 - np.sum(transition_matrix[121, 0:120])

transition_matrix[122, 0:40] = double_roll_matrix[20, :] + ordinary_roll_matrix[20, :]

transformaEmFracaoEPrintar(transition_matrix)
corretude(transition_matrix, 'teste')

# Distribuição Estacionaria
# ein_value, ein_vec = la.eig(transition_matrix.T, right=False, left=True)
# ss_vec = np.power(ein_vec[:, (np.abs(ein_value - 1)) < 1e-6], 2)
# ss_vec[0:40] = ss_vec[0:40] + ss_vec[40:80] + ss_vec[80:120]
# ss_vec[40] = np.sum(ss_vec[120:122])
#
# ss_vec = (ss_vec[0:41]).real
# # ss_vec = (ss_vec / sum(ss_vec)).real
#
# for counter, element in enumerate(ss_vec):
#     print(f'P(x={counter}): {element}')

ein_value, ein_vec = la.eig(transition_matrix.conjugate().T)
ss_vec = ein_vec[:, 0]
ss_vec = (ss_vec / sum(ss_vec)).real

for counter, element in enumerate(ss_vec):
    print(f'P(x={counter}): {element:.5f}')
