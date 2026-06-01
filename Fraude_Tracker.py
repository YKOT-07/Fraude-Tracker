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
# GÉNÉRATEUR DE G'
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

def extraire_sous_graphe(G, sommets):
	sous_graphe = nx.MultiGraph()
	
	sous_graphe.add_nodes_from(sommets)
	
	for u, v in G.edges():
		if u in sommets and v in sommets:
			sous_graphe.add_edge(u, v)
	
	return sous_graphe

def optimisation_de_G(G):
	# Supprimer les boucles et multi-arêtes
	u_new = None
	v_new = None
	for u, v in list(G.edges()):
		if u == v:
			G.remove_edge(u, v)
		
		if u_new == u and v_new == v:
			G.remove_edge(u, v)
		u_new = u
		v_new = v
	
	# Garder la plus grande composante connexe
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
# RECHERCHE DE CLIQUE
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
# MAIN
# ============================================================================

if __name__ == "__main__":
	N = 5000
	p = (math.log(N) + 5) / N
	
	print("=" * 70)
	print("GÉNÉRATION DE G(N, p)")
	print("=" * 70)
	print(f"N = {N} sommets")
	print(f"p = {p:.6f}")
	
	G = generateur_de_G(N, p)
	print(f"G: {G.number_of_nodes()} sommets, {G.number_of_edges()} arêtes")
	
	print("\n" + "=" * 70)
	print("OPTIMISATION DE G → G'")
	print("=" * 70)
	G_prime = optimisation_de_G(G)
	print(f"G': {G_prime.number_of_nodes()} sommets, {G_prime.number_of_edges()} arêtes")
	print(f"Connexe: {nx.is_connected(G_prime)}")
	
	print("\n" + "=" * 70)
	print("COLORATION DE G'")
	print("=" * 70)
	couleurs, nb_couleurs = coloration_graphe(G_prime)
	print(f"Nombre de couleurs utilisées: {nb_couleurs}")
	
	# Statistiques de coloration
	distribution_couleurs = {}
	for couleur in couleurs.values():
		distribution_couleurs[couleur] = distribution_couleurs.get(couleur, 0) + 1
	
	print("\nDistribution des couleurs:")
	for couleur in sorted(distribution_couleurs.keys()):
		print(f"  Couleur {couleur}: {distribution_couleurs[couleur]} sommets")

	print("\n" + "=" * 70)
	print("RECHERCHE DES CLIQUES")
	print("=" * 70)

	cliques = recherche_cliques(G_prime)

	print(f"Nombre de cliques trouvées : {len(cliques)}")

	cliques.sort(key=len, reverse=True)
	for i, clique in enumerate(cliques):
	    print(
	        f"Clique {i+1} "
	        f"(taille {len(clique)}) : {clique}"
	    )