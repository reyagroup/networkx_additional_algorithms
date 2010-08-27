import itertools

TRIAD_NAMES = ("003", "012", "102", "021D","021U", "021C", "111D", "111U", "030T", "030C", "201", "120D","120U", "120C", "210", "300")
TRICODES = (1, 2, 2, 3, 2, 4, 6, 8, 2, 6, 5, 7, 3, 8, 7, 11, 2, 6, 4, 8, 5, 9, 9, 13, 6, 10, 9, 14, 7, 14, 12, 15, 2, 5, 6, 7, 6, 9, 10, 14, 4, 9, 9, 12, 8, 13, 14, 15, 3, 7, 8, 11, 7, 12, 14, 15, 8, 14, 13, 15, 11, 15, 15, 16)
TRICODE_TO_NAME = dict((i,TRIAD_NAMES[TRICODES[i]-1]) for i in xrange(len(TRICODES)))

def _tricode(graph,v,u,w):
	combos = ((v,u,1),(u,v,2),(v,w,4),(w,v,8),(u,w,16),(w,u,32))
	links = ((graph.has_edge(c[0],c[1]),c[2]) for c in combos)
	return sum(x[1] for x in links if x[0])

def getTriadicCensus(graph):
	count = dict((n,0) for n in TRIAD_NAMES)
	for vi,v in enumerate(graph):
		for u in set(itertools.chain(graph.predecessors(v),graph.successors(v))):
			ui = graph.nodes().index(u)
			if ui<=vi : continue
			neighbors = set(itertools.chain(graph.successors(v),graph.successors(u),graph.predecessors(u),graph.predecessors(v)))
			neighbors.remove(u)
			neighbors.remove(v)
			
			if graph.has_edge(u,v) and graph.has_edge(v,u):
				count["102"] += len(graph) - len(neighbors) - 2 
			else:
				count["012"] += len(graph) - len(neighbors) - 2	
			
			for w in neighbors:
				wi = graph.nodes().index(w)
				if ui<wi or(vi<wi and wi<ui and not v in graph.predecessors(w) and not v in graph.successors(w)):
					code = _tricode(graph,v,u,w)
					count[TRICODE_TO_NAME[code]] +=1
	return count