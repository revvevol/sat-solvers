#! /usr/bin/python3

# Ce TP nécessite l'installation de python-sat.
# Pour cela il faut taper la commande suivant dans un console shell :
# pip3 install python-sat

from pysat.solvers import Minisat22

# Définition des variables utilisées

largeur = 7

# NB : on fait varier les valeurs des nombres possibles entre 0 et largeur^2.
# Ici entre 0 et 46. Il faut faire attention à cela lorsque l'on représente la
# grille ou lorsque l'on affiche le résultat

nombres = range(largeur**2)

coord = range(largeur)


def encode(i, j, k):
    return 1 + k + (i + j * largeur) * largeur**2


def decode(n):
    m = n-1
    n1 = m // largeur ** 2
    return (n1 % largeur, n1 // largeur, m % largeur**2)


# Chaque case est occupée par au moins un nombre

phi1 = [[encode(i, j, k) for k in nombres] for i in coord for j in coord]

# Chaque case contient au plus un nombre

phi2 = [[-encode(i, j, k1), -encode(i, j, k2)]
        for i in coord for j in coord for k1 in nombres for k2 in nombres if k1 < k2]

# Chaque nombre apparaît au moins une fois dans la grille

phi3 = [[encode(i, j, k) for i in coord for j in coord] for k in nombres]

# Chaque nombre appraît au plus une fois dans la grille

phi4 = [[-encode(i1, j1, k), -encode(i2, j2, k)]
        for i1 in coord for j1 in coord for i2 in coord for j2 in coord
        for k in nombres if i1 < i2 or j1 < j2]

# Chaque nombre k est voisin du nombre k+1. Essayez de profiter des facilités
# d'écriture que python peut vous apporter.

used = []

def voisin(i1, j1, i2, j2):
    k = []
    used = []
    t = (i2,j2)

    k = [(i1, j1-1), (i1, j1+1), (i1-1, j1), (i1-1, j1-1),
         (i1-1, j1+1), (i1+1, j1), (i1+1, j1-1), (i1+1, j1+1)]

    k = [x for x in k if (x[0] >= 0 and x[1] >= 0) and (x[0] <= 6 and x[1] <= 6) and x not in used]

    if t in k:
        used.append(t)
        return True
    else:
        return False

phi5 = [[-encode(i1, j1, k), -encode(i2, j2, k+1)]
        for k in nombres
        for i1 in coord for j1 in coord
        for i2 in coord for j2 in coord
        if voisin(i1, j1, i2, j2)
        ]

# Contrainte associée à la grille de l'énoncé. Attention aux indices utilisés.

grid = [
    [0, 0, 0, 45, 0, 0, 0],
    [49, 0, 0, 0, 0, 0, 37],
    [30, 0, 0, 0, 0, 0, 12],
    [0, 0, 0, 16, 0, 0, 0],
    [19, 0, 0, 0, 0, 0, 40],
    [1, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 4, 0, 0, 0],
]

phi6 = [[encode(i, j, grid[i][j]-1)]
        for i in coord for j in coord if grid[i][j] != 0]

# Représenter à partir de formules SAT construite une formule SAT qui permette
# de résoudre le problème de l'énoncé :
# 1. commencez par utiliser toutes les contraintes
# 2. enlevez la contrainte phi4
# Que constatez vous ? Comment l'expliquer ?

psi = phi1 + phi2 + phi3 + phi4 + phi5 + phi6


# Adaptez le code afin de pouvoir résoudre la grille suivante :
#
# |    |    | 60 |    | 68 | 67 | 64 |    |   1 |    |
# |    |    |    | 69 |    |    |    |    |     |  5 |
# |    |    |    | 42 | 55 |    |    |    |   4 |    |
# | 76 |    |    |    |    |    |    |    |     |  9 |
# | 77 |    |    | 38 |    |    | 49 | 12 |  10 |    |
# |    | 79 |    |    |    | 48 |    |    | 100 |    |
# | 80 |    |    |    | 35 |    |    |    |  15 |    |
# |    | 84 | 31 |    |    | 24 |    |    |  96 |    |
# | 86 | 85 |    | 27 | 92 |    |    |    |     | 18 |
# |    |    | 90 |    |    |    |    |    |     |    |


# Cette partie du programme lance le solveur SAT avec la conjonction des contraintes,
# c'est-à-dire la concaténation des listes les représentant.
with Minisat22(bootstrap_with=psi) as m:
    # si on trouve une solution
    if m.solve():
        model = [decode(v) for v in m.get_model() if v > 0]  # on récupère les
        # variables qui sont
        # vraies dans la solution
        # trouvée
        # On affiche le résultat lisiblement
        r = [[0 for i in coord] for j in coord]
        for (i, j, k) in model:
            r[i][j] += k+1
        print("\n")
        for ligne in r:
            l = ""
            for nb in ligne:
                if nb < 10:
                    l += "| " + str(nb)
                else:
                    l += "|" + str(nb)
            l += "|"
            print(l)
    else:
        print("pas de solution")
