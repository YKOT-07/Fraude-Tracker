import matplotlib.pyplot as plt
import networkx as nx
import random
import math

# ============================================================================
# GÉNÉRATEUR DE G
# ============================================================================

def generateur_de_G(N, p):
    G = nx.MultiGraph()
    G.add_nodes_from(range(N))

    for i in range(N):
        for j in range(N):
            if random.random() < p:
                G.add_edge(i, j)

    return G

# ============================================================================
# RECHERCHE DES COMPOSANTES CONNEXES
# ============================================================================

def trouver_composantes_connexes(G):
    visites = set()
    composantes = []

    def dfs(sommet, composante):
        pile = [sommet]

        while pile:

            u = pile.pop()
            if u in visites:
                continue

            visites.add(u)
            composante.add(u)

            for v in G.neighbors(u):
                if v not in visites:
                    pile.append(v)

    for sommet in G.nodes():
        if sommet not in visites:
            composante = set()
            dfs(sommet, composante)
            composantes.append(composante)

    return composantes

# ============================================================================
# EXTRACTION D'UN SOUS-GRAPHE
# ============================================================================

def extraire_sous_graphe(G, sommets):
    sous_graphe = nx.MultiGraph()

    sous_graphe.add_nodes_from(sommets)

    for u, v in G.edges():
        if u in sommets and v in sommets:
            sous_graphe.add_edge(u, v)

    return sous_graphe

# ============================================================================
# OPTIMISATION DE G
# ============================================================================

def optimisation_de_G(G):
    # Suppression des boucles
    for u, v in list(G.edges()):
        if u == v:
            G.remove_edge(u, v)

    # Suppression des multi-arêtes
    aretes_vues = set()
    for u, v in list(G.edges()):
        arete = tuple(sorted((u, v)))
        if arete in aretes_vues:
            G.remove_edge(u, v)

        else:
            aretes_vues.add(arete)

    # Recherche des composantes connexes
    composantes = trouver_composantes_connexes(G)

    plus_grande_composante = max(composantes, key=len)

    G_connexe = extraire_sous_graphe(G, plus_grande_composante)

    return G_connexe

# ============================================================================
# COLORATION DU GRAPHE
# ============================================================================

def coloration_graphe(G):
    couleurs = {}

    for sommet in G.nodes():
        couleurs_voisins = set()

        for voisin in G.neighbors(sommet):
            if voisin in couleurs:
                couleurs_voisins.add(couleurs[voisin])

        couleur = 1
        while couleur in couleurs_voisins:
            couleur += 1

        couleurs[sommet] = couleur

    nb_couleurs = len(set(couleurs.values()))

    return couleurs, nb_couleurs

# ============================================================================
# RECHERCHE DES CLIQUES
# ============================================================================

def est_voisin_de_tous(G, sommet, clique):

    for v in clique:
        if v == sommet:
            continue

        if not G.has_edge(sommet, v):
            return False

    return True

def recherche_cliques(G):

    cliques = []

    for u in G.nodes():

        clique = {u}

        voisins = list(G.neighbors(u))

        for v in voisins:
            if est_voisin_de_tous(G, v, clique):
                clique.add(v)

        if len(clique) >= 3:
            clique_triee = tuple(sorted(clique))

            if clique_triee not in cliques:
                cliques.append(clique_triee)

    return cliques

# ============================================================================
# ANALYSE DES SOMMETS
# ============================================================================

def analyser_sommets(G, cliques):
    analyse = {}
   
    for sommet in G.nodes():
        degre = G.degree(sommet)

        nb_cliques = 0
        for clique in cliques:
            if sommet in clique:
                nb_cliques += 1

        score = degre + 5 * nb_cliques

        if score < 10:
            categorie = "Consommateur"

        elif score < 25:
            categorie = "Intermediaire"

        else:
            categorie = "Fournisseur"

        analyse[sommet] = {
            "degre": degre,
            "nb_cliques": nb_cliques,
            "score": score,
            "categorie": categorie
        }

    return analyse

# ============================================================================
# VISUALISATION
# ============================================================================

def afficher_graphe(
    G,
    couleurs
):

    couleurs_affichage = []

    for sommet in G.nodes():
        couleurs_affichage.append(
            couleurs[sommet]
        )

    plt.figure(
        figsize=(12, 8)
    )

    position = nx.spring_layout(
        G,
        seed=42
    )

    nx.draw(
        G,
        pos=position,
        node_color=couleurs_affichage,
        node_size=50,
        with_labels=False
    )

    plt.title(
        "Graphe colore"
    )

    plt.show()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":

    N = 1000
    p = (math.log(N) + 5) / N

    print("=" * 70)
    print("GENERATION DE G(N,p)")
    print("=" * 70)

    print(f"N = {N}")
    print(f"p = {p:.6f}")

    G = generateur_de_G(N, p)

    print(f"G : "f"{G.number_of_nodes()} sommets, "f"{G.number_of_edges()} aretes")

    print("\n" + "=" * 70)
    print("OPTIMISATION DE G")
    print("=" * 70)

    G_prime = optimisation_de_G(G)

    print(f"G' : "f"{G_prime.number_of_nodes()} sommets, "f"{G_prime.number_of_edges()} aretes")

    print(f"Connexe : "f"{nx.is_connected(G_prime)}")

    degres = [G_prime.degree(s) for s in G_prime.nodes()]

    degre_moyen = (sum(degres)/ len(degres))

    degre_max = max(degres)

    n = G_prime.number_of_nodes()
    m = G_prime.number_of_edges()

    densite = (2 * m / (n * (n - 1)))

    print("\n" + "=" * 70)
    print("STATISTIQUES")
    print("=" * 70)

    print(f"Degre moyen : "f"{degre_moyen:.2f}")

    print(f"Degre maximal : "f"{degre_max}")

    print(f"Densite : "f"{densite:.4f}")

    print("\n" + "=" * 70)
    print("COLORATION")
    print("=" * 70)

    couleurs, nb_couleurs = coloration_graphe(G_prime)

    print(f"Nombre de couleurs : "f"{nb_couleurs}")

    print("\n" + "=" * 70)
    print("RECHERCHE DES CLIQUES")
    print("=" * 70)

    cliques = recherche_cliques(G_prime)

    print(f"Nombre de cliques : "f"{len(cliques)}")

    if cliques:

        plus_grande = max(cliques,key=len)

        print(f"Taille maximale : "f"{len(plus_grande)}")

    print("\n" + "=" * 70)
    print("ANALYSE DES SOMMETS")
    print("=" * 70)

    analyse = analyser_sommets(G_prime,cliques)

    suspects = []

    for sommet, infos in analyse.items():
        if infos["score"] >= 25:
            suspects.append((sommet, infos))

    suspects.sort(key=lambda x:x[1]["score"],reverse=True)

    print(f"Nombre de suspects : "f"{len(suspects)}")

    print("\nTOP 10 DES SOMMETS LES PLUS SUSPECTS\n")

    for sommet, infos in suspects[:10]:

        print(
            f"Sommet {sommet}"
            f" | Degre={infos['degre']}"
            f" | Cliques={infos['nb_cliques']}"
            f" | Score={infos['score']}"
            f" | {infos['categorie']}"
        )

    print("\nAffichage du graphe...")

    afficher_graphe(G_prime,couleurs)
