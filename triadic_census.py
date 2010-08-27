"""
Determines the triadic census of a graph

"""

__author__ = """Alex Levenson (alex@isnontinvain.com)\nDiederik van Liere (diederik.vanliere@rotman.utoronto.ca)"""
#	(C) Reya Group: http://www.reyagroup.com
#	Alex Levenson (alex@isnotinvain.com)
#	Diederik van Liere (diederik.vanliere@rotman.utoronto.ca)
#	BSD license.

__all__ = ["triadic_census"]

import itertools

TRIAD_NAMES = ("003", "012", "102", "021D","021U", "021C", "111D", "111U", "030T", "030C", "201", "120D","120U", "120C", "210", "300")
TRICODES = (1, 2, 2, 3, 2, 4, 6, 8, 2, 6, 5, 7, 3, 8, 7, 11, 2, 6, 4, 8, 5, 9, 9, 13, 6, 10, 9, 14, 7, 14, 12, 15, 2, 5, 6, 7, 6, 9, 10, 14, 4, 9, 9, 12, 8, 13, 14, 15, 3, 7, 8, 11, 7, 12, 14, 15, 8, 14, 13, 15, 11, 15, 15, 16)
TRICODE_TO_NAME = dict((i,TRIAD_NAMES[TRICODES[i]-1]) for i in xrange(len(TRICODES)))

def _tricode(G,v,u,w):
	"""
	This is some fancy magic that comes from Batagelj and Mrvar's paper.
	It treats each link between v,u,w as a bit in the binary representation of an integer
	This number then is mapped to wich of the 16 triad types it represents
	"""
	combos = ((v,u,1),(u,v,2),(v,w,4),(w,v,8),(u,w,16),(w,u,32))
	links = ((G.has_edge(c[0],c[1]),c[2]) for c in combos)
	return sum(x[1] for x in links if x[0])

def triadic_census(G):
	"""
	Determines the triadic census of a graph

	Triadic census is a count of how many of the 16 possible types of triad are present in a graph.
	
	Parameters
	----------
	G : graph
		A networkx graph
		
	Returns
	-------
	census : dictionary
			 Dictionary with triad names as keys and number of occurances as values

	Refrences
	---------
	.. [1] A subquadratic triad census algorithm for large sparse networks with small maximum degree
	   Vladimir Batagelj and Andrej Mrvar University of Ljubljana
	   http://vlado.fmf.uni-lj.si/pub/networks/doc/triads/triads.pdf
	"""
	
	# this algorithm requires the nodes be integers from 0 to n, so we use the node's indexes in G.nodes()
	
	# initialze the count to zero
	count = dict((n,0) for n in TRIAD_NAMES)
	for vi,v in enumerate(G):
		for u in set(itertools.chain(G.predecessors(v),G.successors(v))):
			ui = G.nodes().index(u)
			if ui<=vi : continue
			neighbors = set(itertools.chain(G.successors(v),G.successors(u),G.predecessors(u),G.predecessors(v)))
			neighbors.remove(u)
			neighbors.remove(v)
			
			# calculate dyadic triads instead of counting them
			if G.has_edge(u,v) and G.has_edge(v,u):
				count["102"] += len(G) - len(neighbors) - 2 
			else:
				count["012"] += len(G) - len(neighbors) - 2	
			
			# count connected triads
			for w in neighbors:
				wi = G.nodes().index(w)
				if ui<wi or(vi<wi and wi<ui and not v in G.predecessors(w) and not v in G.successors(w)):
					code = _tricode(G,v,u,w)
					count[TRICODE_TO_NAME[code]] +=1
	
	# null triads = total number of possible triads - all found triads		
	n = len(G)
	count["003"] = ((n * (n-1) * (n-2)) / 6) - sum(count.values())
	return count