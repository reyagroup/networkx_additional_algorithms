# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Monday August 16th

from infomap import findBestPartition
from ..agreement import findAgreementBetween
from igraph import Graph as iGraph

def newmanEigenvector(graph):
	ig = iGraph()
	ig.add_vertices(len(g)-1)
	ig.add_edges([(g.nodes().index(edge[0]),g.nodes().index(edge[1])) for edge in g.edges()])
	res = ig.community_leading_eigenvector()

	part = {}
	for c in xrange(len(res)):
		for i in res[c]:
			part[g.nodes()[i]] = c

	return part

def modularity(graph,partition):
	modularity = 0.0
	A = nx.convert.to_numpy_matrix(graph)
	twoM = float(graph.number_of_edges())*2
	for i in xrange(len(A)):
		for j in xrange(len(A)):
			if partition[graph.nodes()[i]] == partition[graph.nodes()[j]]:
				modularity += A[i,j] - float(graph.degree(graph.nodes()[i]) * graph.degree(graph.nodes()[i]))/twoM
	return (1.0/twoM) * modularity

def repeatedInfomap(graph,numTrials=10,setSimilarityThreshold=0.8,voteThreshold=0.8,returnFullHistogram=False):
	"""
	runs the infomap community detection algorithm numTrials times, and returns the "agreement" between the runs
	
	graph: a networkx graph

	numTrials: number of runs of the infomap algorithm

	setSimilarityThreshold,voteThreshold: see findAgreementBetween
	
	returns a dictionary mapping node->[list of communities node belongs to]
	if returnFullHistogram is set to True, then voteThreshold will be ignored and a list of tuples will be returned
	in the form, for every community, (community representative, number of trials that 'voted' for this community)
	
	A 'representative' will be chosen for each community, and it will be the set that is present in the return value.
	It is the one which has the highest similarity to all the other sets in it's super-class
	"""
	runs = [findBestPartition(graph,partitionOnly=False) for t in xrange(numTrials)]
	trials = [c[1].values() for c in runs]
	
	agree = findAgreementBetween(trials,setSimilarityThreshold=setSimilarityThreshold,voteThreshold=voteThreshold,returnFullHistogram=returnFullHistogram)
	
	if returnFullHistogram:
		return agree
	
	partition = {}
	for cet in xrange(len(agree)):
		for node in agree[cet]:
			if node not in partition:
				partition[node] = []
			partition[node].append(cet)
			
	return partition