# -*- coding: utf-8 -*-
"""

@author: alper

StabTraj.py v1

"""

import numpy as np
import matplotlib.pyplot as plt

# TRAITEMENT DES RESULTATS FOURNIS PAR AEROLAB ET AFFICHAGE DES COEFFICIENTS DANS LE DIAGRAMME DE STABILITE

# les conditions pour être stable sont les suivantes :
# 15 <  Cn   < 40
#  2 <  MS   < 6
# 40 < Cn*MS < 100
# 10 < finesse < 35

# DONNEES A SAISIR PAR L UTILISATEUR

# CARACTERISTIQUES DE LA FUSEE

# A MODIFIER

Dref = 83; # diamètre de la fusée en mm
CdGvide = 741.9275; # centre de gravité avec propu vide
CdGplein = 815.6473; # centre de gravité avec propu plein
Ltot = 1309; # longeur totale de la fusée en mm

# RECUPERATION DES DONNEES

cd_data = np.loadtxt("cd_corr", skiprows=1)
cn_data = np.loadtxt("cn_corr", skiprows=1)
xcp_data = np.loadtxt("xcp_corr", skiprows=1)

## Récuperation des données OK
Mach1 = cn_data[:, 0]
CN = cn_data[:, 1]
Mach2 = xcp_data[:, 0]
XCP = xcp_data[:, 1]
Mach3 = cd_data[:, 0]
CD = cd_data[:, 1]

# CRITERES DE STABILITE
# cnalpha
min_cn = 15
max_cn = 40
# marge statique
min_ms = 2
max_ms = 6
# produit cn*ms
min_couple = 40
max_couple = 100
# finesse
min_finesse = 10
max_finesse = 35

# AUTRE INFOS
c = 340  # vitesse du son en m/s
graphes_mach = 1  # prend la valeur 1 si on veut afficher chaque coefficient en fonction du mach, 0 sinon
graphes_cd = 1  # prend la valeur 1 si on veut afficher la traînée en fonction du mach/vitesse, 0 sinon
graphe_stabilite = 1  # prend la valeur 1 si on veut afficher le diagramme de stabilite , 0 sinon

# CALCUL
if graphes_mach == 1:
    # plot du COEFFICIENT DE PORTANCE
    plt.figure(1)
    plt.subplot(2, 3, 1)
    plt.plot(Mach1, CN)
    plt.plot([Mach1[0], Mach1[-1]], [min_cn, min_cn], '--r', linewidth=2)
    plt.plot([Mach1[0], Mach1[-1]], [max_cn, max_cn], '--r', linewidth=2)
    plt.grid(True)
    plt.title('Cnalpha')
    plt.xlabel('Mach')
    plt.ylabel('Cn')

    # plot de la POSITION DU CENTRE DE POUSSEE et plot de la marge statique

    # XCP
    plt.subplot(2, 3, 2)
    plt.plot(Mach2, XCP)
    plt.grid(True)
    plt.title('Position du centre de poussée')
    plt.xlabel('Mach')
    plt.ylabel('XCP (mm)')

    # MARGE STATIQUE
    plt.subplot(2, 3, 3)
    marge_vide = (XCP - CdGvide) / Dref
    marge_plein = (XCP - CdGplein) / Dref
    plt.plot(Mach2, marge_vide)
    plt.plot(Mach2, marge_plein)
    plt.plot([Mach2[0], Mach2[-1]], [min_ms, min_ms], '--r', linewidth=2)
    plt.plot([Mach2[0], Mach2[-1]], [max_ms, max_ms], '--r', linewidth=2)
    plt.grid(True)
    plt.title('Marge statique')
    plt.xlabel('Mach')
    plt.ylabel('Marge statique (en calibre)')
    plt.legend(['avec propulseur vide', 'avec propulseur plein'])

    # plot du COUPLE : produit des CN et MS

    plt.subplot(2, 1, 2)  # Subplot 1
    couple_vide = CN * marge_vide
    couple_plein = CN * marge_plein
    plt.plot(Mach1, couple_vide)
    plt.plot(Mach1, couple_plein)
    plt.plot([Mach1[0], Mach1[-1]], [40, 40], '--r', linewidth=2)
    plt.plot([Mach1[0], Mach1[-1]], [100, 100], '--r', linewidth=2)
    plt.title('Cnalpha * Marge statique')
    plt.grid(True)
    plt.xlabel('Mach')
    plt.ylabel('Cn*MS')
    plt.xticks(np.arange(0, max(Mach1), (len(Mach1) - 1) / 400))
    plt.legend(['avec propulseur vide', 'avec propulseur plein'])
    plt.tight_layout()  # Adjust the layout of subplots

# SI OUTPUT GRAPHIQUE EST VOULU
if graphes_cd == 1:

    plt.figure(2)
    plt.subplot(2, 1, 1)
    plt.plot(Mach3, CD, '.r', markersize=6)
    plt.grid(True)
    plt.title('Coefficient de traînée en fonction du nombre de Mach')
    plt.xlabel('Mach')
    plt.ylabel('Cd')
    plt.legend(['Aerolab'])

    plt.subplot(2, 1, 2)
    Vit3 = Mach3 * c
    plt.plot(Vit3, CD, '.r', markersize=6)
    plt.plot(Vit3, np.interp(Vit3, Vit3, CD), '-b')
    plt.grid(True)
    plt.title('Coefficient de traînée en fonction de la vitesse')
    plt.xlabel('Vitesse (m/s)')
    plt.ylabel('Cd')
    plt.legend(['Aerolab', 'Interpolation'])
    
    plt.tight_layout()

# DIAGRAMME DES CRITERES DE STABILITE

if graphe_stabilite == 1:
    plt.figure(3)

    X = [0, max_ms + 1]
    Y = [0, max_cn + 10]

    plt.plot(marge_vide, CN, linewidth=2)
    plt.plot(marge_plein, CN, linewidth=2)
    plt.legend(['propulseur vide', 'propulseur plein'])

    finesse = Ltot / Dref

    X1 = [min_ms, min_ms]
    plt.plot(X1, Y, 'r-', label='_nolegend_')
    y1 = [min_couple / min_ms, max_cn]
    plt.plot(X1, y1, 'r-', label='_nolegend_', linewidth=2)
    X2 = [max_ms, max_ms]
    plt.plot(X2, Y, 'r-', label='_nolegend_')
    y2 = [min_cn, max_couple / max_ms]
    plt.plot(X2, y2, 'r-', label='_nolegend_', linewidth=2)

    plt.axis([X[0], X[1], Y[0], Y[1]])
    plt.title('Diagramme de stabilité, données Aerolab', fontsize=16)

    if min_finesse < finesse < max_finesse:
        plt.annotate('FINESSE OK',
                 xy=(0.5, 0.7),
                 xycoords='axes fraction',
                 fontsize=10,
                 bbox=dict(boxstyle='round', facecolor='green', edgecolor='green', alpha=0.5))
    else:
        plt.annotate('FINESSE NOK',
                 xy=(0.6, 0.6),
                 xycoords='axes fraction',
                 fontsize=10,
                 bbox=dict(boxstyle='round', facecolor='red', edgecolor='red', alpha=0.5))

    plt.xlabel('Marge Statique (MS)')
    plt.ylabel('Portance Cnalpha')

    Y1 = [min_cn, min_cn]
    plt.plot(X, Y1, 'r-', label='_nolegend_')
    x1 = [min_couple / min_cn, max_ms]
    plt.plot(x1, Y1, 'r-', label='_nolegend_', linewidth=2)

    Y2 = [max_cn, max_cn]
    plt.plot(X, Y2, 'r-', label='_nolegend_')
    x2 = [min_ms, max_couple / max_cn]
    plt.plot(x2, Y2, 'r-', label='_nolegend_', linewidth=2)

    x = np.arange(0, max_ms + 1, 0.01)

    y1 = min_couple / x
    plt.plot(x, y1, 'r-', label='_nolegend_')
    x1 = np.arange(min_ms, min_couple / min_cn, 0.01)
    y1 = min_couple / x1
    plt.plot(x1, y1, 'r-', label='_nolegend_', linewidth=2)

    y2 = max_couple / x
    plt.plot(x, y2, 'r-', label='_nolegend_')
    y2 = np.arange(max_couple / max_ms, max_cn, 0.01)
    x2 = max_couple / y2
    plt.plot(x2, y2, 'r-', label='_nolegend_', linewidth=2)

    plt.scatter(marge_plein, CN, 100, Mach1, '.', label='_nolegend_')
    plt.scatter(marge_vide, CN, 100, Mach1, '.', label='_nolegend_')
    echelle = plt.colorbar()
    echelle.set_label('Mach', fontsize=13)

    plt.xlim([1, 7])
    plt.ylim([10, 45])

minMS_vide = min(marge_vide)
maxMS_vide = max(marge_vide)
minMS_plein = min(marge_plein)
maxMS_plein = max(marge_plein)
minCN = min(CN)
maxCN = max(CN)
minPROD_vide = minMS_vide * minCN
maxPROD_vide = maxMS_vide * maxCN
minPROD_plein = minMS_plein * minCN
maxPROD_plein = maxMS_plein * maxCN

plt.show()