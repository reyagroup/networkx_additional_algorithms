#!nodens-python
import networkx as nx
import numpy
import csv

def _proportionalTieStrength(A,Vi,i,j):
	"""
	Calculates P from Burt's equation
	
	A is the adjacencey matrix
	Vi is a list of i' s neighbors as indexices in A
	i and j are two nodes in A
	"""
	num =  (A.item(i,j) + A.item(j,i))
	denom = 0.0
	for k in Vi:
		if k==i: continue
		denom += A.item(i,k) + A.item(k,i)
	return num/denom

def _calcProportionalTieStrengths(A):
	"""
	Calculates P from Burt's equation

	A is the adjacencey matrix
	"""
	num = A.copy()
	num = num + num.transpose()

	denom = num.sum(1)
	denom = numpy.repeat(denom,len(num),axis=1)
	return numpy.divide(num,denom)

def _neighborsIndexes(graph,node,includeInLinks,includeOutLinks):
	"""
	returns the neighbors of node in graph
	as a list of their INDEXes within graph.node()
	"""
	neighbors = set()
	
	if includeOutLinks:
		neighbors |= set(graph.neighbors(node))
	
	if includeInLinks:
		neighbors |= set(graph.predecessors(node))
		
	return map(lambda x : graph.nodes().index(x),neighbors)

def calcConstraints(graph,includeInLinks=False,includeOutLinks=True,wholeNetwork=True):
	"""
	Calculate Burt's constraint on each node in graph.
	
	graph: a networkx Graph or DiGraph
	includeInLinks: whether each ego network should include nodes which point to the ego - this should be False for undirected graphs
	includeOutLinks: whether each ego network should include nodes which the ego points to - this should be True for undirected graphs
	wholeNetwork: whether to use the whole ego network for each node, or only the overlap between the current ego's network and the other's ego network
	"""
		
	# get the adjacency matrix view of the graph
	# which is a numpy matrix
	A = nx.convert.to_numpy_matrix(graph)
	
	# calculate P_i_j from Burt's equation
	p = _calcProportionalTieStrengths(A)
	
	# this is the return value
	constraints = {}
	
	for node in graph.nodes():
		# each element of constraints will be a dictionary of this form
		# unless the node in question is an isolate in which case it
		# will be None
		constraint = {"C-Index": 0.0 ,"C-Size": 0.0, "C-Density": 0.0, "C-Hierarchy": 0.0}
		
		# Vi is the set of i's neighbors
		Vi = _neighborsIndexes(graph,node,includeInLinks,includeOutLinks)
		if len(Vi) == 0:
			# isolates have no defined constraint
			constraints[node] = None
			continue
		
		# i is the node we are calculating constraint for
		# and is thus the ego of the ego net	
		i = graph.nodes().index(node)

		for j in Vi:
			Pij = p[i,j]
			constraint["C-Size"] += Pij ** 2
			
			innerSum = 0.0
			for q in Vi:
				if q == j or q == i: continue
				Vq = _neighborsIndexes(graph,graph.nodes()[q],includeInLinks,includeOutLinks)
				if not wholeNetwork:
					Vq = set(Vq)
					ViSet = set(Vi)
					ViSet.add(i)
					Vq &= ViSet
					innerSum += p[i,q] * _proportionalTieStrength(A,Vq,q,j)
				else:
					innerSum += p[i,q] * p[q,j]
			
			constraint["C-Hierarchy"] += innerSum ** 2
			constraint["C-Density"] += 2*Pij*innerSum
		
		constraint["C-Index"] = constraint["C-Size"] + constraint["C-Density"] + constraint["C-Hierarchy"] 
		constraints[node] = constraint
	return constraints

def writeConstraints(constraints,file):
	file = nx.utils._get_fh(file, mode='w')

	writer = csv.writer(file)
	writer.writerow(["Node","Constraint","C-Size","C-Density","C-Hierarchy"])
	for i in constraints:
		writer.writerow([i,constraints[i]["C-Index"],constraints[i]["C-Size"],constraints[i]["C-Density"],constraints[i]["C-Hierarchy"]])
	file.close
