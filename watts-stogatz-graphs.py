# -*- coding: utf-8 -*-

import networkx as nx
import random
import matplotlib.pyplot as plt 

def create_graph(n, k, p):

	G=nx.Graph()

	#aufbauen des Watts-Strogatz-Graphen
	G.add_cycle(range(0,n))
	nodes=G.nodes()

	for i in nodes:
	    for kk in range(1,k+1):
		if(i+kk<len(nodes)-1):
			G.add_edge(nodes[i],nodes[i+kk])
		else:
			index=(i+kk)%(len(nodes))
			G.add_edge(nodes[i],nodes[index])
	#für jede kante einmal würfeln ist das gleiche wie:
	#zufällig n*p (abgerundet) kanten auszuwählen
	random_e=random.sample(G.edges(),  k=int(float(n)*p))

	for e in random_e:
		new_end=random.randint(0,n-1)
		while(new_end==e[1]):
			new_end=random.randint(0,n-1)
		G.remove_edge(e[0], e[1])
		G.add_edge(e[0], new_end)
	return (G,nodes)

def get_mean_pathlenght(G,n,nodes):

	mean=0.0
	i=0

	for s in range(0,100):
		start=  random.randint(0,n-1)
		stop=random.randint(0,n-1)
		while(start==stop):
			stop=random.randint(0,n-1)
		path=nx.shortest_path(G, nodes[start],nodes[stop])
		mean=mean+len(path)-1
		i=i+1
	mean_path=mean/i
	#print "Durchschnittliche Pfadlänge aus 100 Knotenpaaren: "+str(mean_path)+" hops"
	return mean_path

def get_mean_clustering(G, n, nodes):

	#Berechnung Clustering Koeffizient unter verwendung von NetworkX funktion
	#val=0
	#for no in nodes:
	#	coef=nx.clustering(G, no)
	#	val=val+coef
	#mean_clustering=val/n

	sum_clus_coef=0;

	for no in nodes:
		nei= G.neighbors(no)
		nr_nei=len(nei)
		potential_nr_edges=(nr_nei*(nr_nei+1))/2
		nr_edges=0
		for i in range(0, len(nei)):
			for j in range(i+1,len(nei)):
				if G.has_edge(i, j):
					nr_edges +=1
		clus_coef=float(nr_edges)/float(potential_nr_edges)
		sum_clus_coef+=clus_coef
	mean_clustering=sum_clus_coef/len(nodes)

	#print "Durchschnittlicher Clustering Coeffizient "+str(mean_clustering)
	return mean_clustering


#Plotten mit logskala für x 
def plotting(pp, path,clust ):
	x=pp
	y1=path
	y2=clust
	
	plt.semilogx(x,y1, 'r')
	plt.semilogx(x,y1, 'bo')
	plt.title("P zur Durschnittlichen Pfadlaenge")
	plt.xlabel('Wahrscheinlichkeit p ')
	plt.ylabel("Dursschnittliche Pfadlaenge")
	plt.xlim(-0.1, 1.1 )
	plt.show()
	
	plt.semilogx(x,y2, 'r')
	plt.semilogx(x,y2, 'bo')
	plt.title("P zum Durschnittlichen Clustering Koeffizient")
	plt.xlabel('Wahrscheinlichkeit p ')
	plt.ylabel("Dursschnittlicher Clustering Koeffizient")
	plt.xlim(-0.1, 1.2 )
	plt.ylim(ymax=0.55 )
	plt.show()


n=5000
k=2
pp=[0.00001, 0.0001, 0.001, 0.01 , 0.1, 1. ]

path=list()
clust=list()
	
for p in pp:

	G,nodes =create_graph(n, k, p)
	mean_path=get_mean_pathlenght(G,n, nodes)
	mean_clustering=get_mean_clustering(G, n, nodes)
	print str(p)+" "+str(mean_path)+" "+str(mean_clustering)

	path.append(mean_path)
	clust.append (mean_clustering)

plotting(pp, path,clust )
#######Auswertung#############

