TRIAD_NAMES = ("003", "012", "102", "021D","021U", "021C", "111D", "111U", "030T", "030C", "201", "120D","120U", "120C", "210", "300")
def getTriadicCensus(graph):
	count = dict((n,0) for n in TRIAD_NAMES)
	
	for node1,node2 in graph.edges():
		v,u = graph.nodes().index(node1),graph.nodes().index(node2)
		neighbors = graph.successors(node1) + graph.successors(node2) + graph.predecessors(node1) + graph.predecessors(node2)
		neighbors = set(neighbors)
		neighbors.remove(node1)
		neighbors.remove(node2)
		if graph.has_edge(node1,node2) and graph.has_edge(node2,node1):
			if v >= u: continue
			count["102"] += len(graph) - len(neighbors) - 2 
		else:
			count["012"] += len(graph) - len(neighbors) - 2
			
	return count
