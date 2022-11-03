'''
    Este é um programa do algoritmo genético de Holland
    para encontrar o número binário dentre do intervalo de
    [0,255] que apresenta a maior ocorrencia da sub string '01'
    * a população é formada por 10 cromossomo
    * o cromossomo é um vetor binário de 8 posições
    * cruzamento de um ponto de corte e probabilidade de cruzamento maior que 60
    * mutação por complemento com probabilidade de mutação maior que 90
    * inversão com probabilidade de inversão de 90
    * seleção elitista, torneio e roleta russa 
    * substituição elitista
'''

from numpy.random import randint
from numpy.random import rand
import numpy as np

POP_SIZE = 10
CHROMO_SIZE = 8
R_CROSSOVER = 0.6
R_MUTATION = 0.9
R_INVERSION = 0.9


def creates_pop(pop_size=POP_SIZE, chromo_size=CHROMO_SIZE):
    pop = np.random.randint(2, size=(pop_size, chromo_size)).tolist()
    return pop


def show_pop(pop):
    print(np.array(pop))


def show_pop_fit(pop, f1):
    for i in range(0, len(pop)):
        print(np.array(pop[i]), " = ", f1[i])


def sort_pop(pop, f1, chromo_size=CHROMO_SIZE):
    for a in range(0, len(pop)-1):
        for b in range(a+1, len(pop)):
            if (f1[a] < f1[b]):
                for i in range(0, chromo_size):
                    aux = pop[a][i]
                    pop[a][i] = pop[b][i]
                    pop[b][i] = aux
                aux = f1[a]
                f1[a] = f1[b]
                f1[b] = aux


def fitness(pop, chromo_size=CHROMO_SIZE):
    f1 = []
    for i in range(len(pop)):
        aux = 0
        for j in range(0, chromo_size-1):
            if (pop[i][j] == 0 and pop[i][j+1] == 1):
                aux += 1
        f1.append(aux)
    return f1


def elitism_selection(pop, f1, k=6):
    sort_pop(pop, f1)
    return pop[:k]


def tournament_selection(pop, f1, k=6):
    selected = []
    for _ in range(k):
        c1 = randint(0, len(pop))
        c2 = randint(0, len(pop))
        if f1[c1] >= f1[c2]:
            selected.append(pop[c1])
        else:
            selected.append(pop[c2])
    return selected


def roulette_selection(pop, f1, k=6):
    aux_roulette = []
    for i in range(len(pop)):
        for _ in range(f1[i]):
            aux_roulette.append(pop[i])

    selected = []
    for _ in range(k):
        c1 = randint(0, len(aux_roulette))
        selected.append(aux_roulette[c1])
    return selected


def crossover(des, selected, r_crossover=R_CROSSOVER):
    for i in range(0, len(selected), 2):
        p1, p2 = selected[i], selected[i+1]
        c1, c2 = p1.copy(), p2.copy()
        if rand() >= r_crossover:
            pt = randint(1, len(p1)-2)
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
        des.append(c1)
        des.append(c2)
    return des


def mutation(selected, des, chromo_size=CHROMO_SIZE, r_mutation=R_MUTATION):
    for a in range(len(selected)):
        aux = []
        for b in range(chromo_size):
            if (rand() >= r_mutation):
                aux2 = 1 - selected[a][b]
                aux.insert(b, aux2)
            else:
                aux.insert(b, selected[a][b])
        des.append(aux)
    return des


def inversion(selected, des, r_inversion=R_INVERSION):
    for a in range(len(selected)):
        aux1 = []
        if (rand() >= r_inversion):  # inversion = 0.9
            aux1 = selected[a].copy()
            p1 = randint(0, 6)  # primeira posição
            p2 = randint(0, 7)  # segunda posição

            while (p2 < p1):
                p2 = randint(0, 7)

            x = p2-p1  # tamanho da área a ser invertida
            if (x % 2 == 0):
                x = int(x/2)
            else:
                x = int((x+1)/2)
            for i in range(0, x):
                aux2 = aux1[p1+i]
                aux1[p1+i] = aux1[p2-i]
                aux1[p2-i] = aux2
            des.append(aux1)
    return des


def substitution(pop, f1, des):
    aux_pop = pop.copy()
    for i in range(len(des)):
        aux_pop.append(des[i])
    aux_f = fitness(aux_pop)
    sort_pop(aux_pop, aux_f)
    pop = aux_pop[:10]
    f1 = aux_f[:10]
    return pop, f1


des = []

print('população atual gerada')
pop = creates_pop()
show_pop(pop)

print('população atual com sua adaptação')
f1 = fitness(pop)
show_pop_fit(pop, f1)

print('população atual na ordem decrescente da adaptação')
sort_pop(pop, f1)
show_pop_fit(pop, f1)

while (f1[0] != 4):
    # selecionar um tipo de seleção
    selected = elitism_selection(pop, f1)
    #selected = tournament_selection(pop, f1)
    #selected = roulette_selection(pop, f1)

    print('cruzamento')
    des = crossover(des, selected)
    show_pop(des)

    print('mutação')
    des = mutation(selected, des)
    show_pop(des)

    print('inversão')
    des = inversion(selected, des)
    show_pop(des)

    print('população descencente com sua adaptação')
    f2 = fitness(des)
    show_pop_fit(des, f2)

    print('população descendente na ordem decrescente da adaptação')
    sort_pop(des, f2)
    show_pop_fit(des, f2)

    print('população nova')
    pop, f1 = substitution(pop, f1, des)
    show_pop_fit(pop, f1)
    des.clear()
