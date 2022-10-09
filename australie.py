#! /usr/bin/python3

# RÃ©solution par l'intermÃ©diaire d'un solveur-SAT du problÃ¨me de coloration
# avec 3 couleurs de la carte d'Australie.

# Pour utiliser ce code, il faut avoir installÃ© pysat :
# pip install python-sat[pblib,aiger]

from pysat.solvers import Minisat22

# DonnÃ©es du problÃ¨me

## Liste des Ã©tats
etats = ["Western Autralia",
         "Nothern Territory",
         "Queensland",
         "South Australia",
         "New South Wales",
         "Victoria",
         "Tasmania"]

## Liste des couleurs
couleurs = ["rouge","vert","bleu"]

## Liste des paires de voisins
voisins =  [("Western Autralia","Nothern Territory"),
           ("Western Autralia","South Australia"),
           ("Nothern Territory", "Queensland"),
           ("Nothern Territory", "South Australia"),
           ("South Australia","Queensland"),
           ("Queensland", "New South Wales"),
           ("South Australia","New South Wales"),
           ("South Australia","Victoria"),
           ("New South Wales","Victoria"),
           ("Victoria","Tasmania")]

# Fonctions pour interagir avec la reprÃ©sentation des variables
# propositionnelles.

def encode(e,c):
    """Renvoie un nombre qui reprÃ©sente la variable propositionnelle pour paire
    (Ã©tat,couleur). Ce nombre est unique et strictement positif pour chaque
    paire.
    """
    ne = len(etats)
    return 1 + etats.index(e) + ne * couleurs.index(c)

def decode(n):
    """Fonction inverse de dÃ©code. Ã‰tant donnÃ© un nombre n reprÃ©sentant une paire
(Ã©tat,couleur), renvoie la paire."""
    m=n-1
    ne = len(etats)
    return (etats[m % ne], couleurs[m//ne])

# Nous reprÃ©sentons les contraintes du problÃ¨me.

## Chaque Ã©tat a au moins une couleur
phi1 = [[encode(e,c) for c in couleurs] for e in etats]

print(phi1)

## Chaque Ã©tat a au plus une couleur
phi2 = [[-encode(e, c1), -encode(e, c2)] for e in etats
        for c1 in couleurs
        for c2 in couleurs
        if c1 < c2]

## Deux Ã©tats voisins ne peuvent avoir la mÃªme couleur
psi = [[-encode(e1, c), -encode(e2, c)] for (e1, e2) in voisins
        for c in couleurs]

# RÃ©solution du problÃ¨me



## On instancie le solver
with Minisat22(bootstrap_with=phi1+phi2+psi) as m:
    # si on trouve une solution
    if m.solve():
        model = [decode(v) for v in m.get_model() if v > 0] # on rÃ©cupÃ¨re les
                                                           # variables qui sont
                                                           # vraies dans la solution
                                                           # trouvÃ©e
        # On affiche le rÃ©sultat lisiblement
        l = max([len(s) for s in etats])
        for (e,c) in model:
            p = l - len(e)
            print(e, " "*(p+1), "-> ", c)