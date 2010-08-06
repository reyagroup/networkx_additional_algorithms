# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Thursday July 29th 2010

# simple discrete core periphery partitioner, based on the paper:
# Computing Core/Periphery Structures and Permutation Tests for Social Relations Data
#                                        by
#               John P. Boyd†, William J. Fitzgerald, and Robert J. Beck
#                  University of California at Irvine, CA 92697, USA


import random
import networkx as nx
import numpy

def partition(graph,partition=None,numIterations=3):
	"""
	Partitions graph into a core set and a periphery set
	using a simple optimizer
	
	graph: a networkx graph
	
	partition: optionally supply a starting partition as a 
	dictionary mapping node->{0,1} (0 for periphery, 1 for core)
	Must be at least one node in each partition
	
	numIterations: how many times to run the optimizer, should be around 2 to five, probably not many more
	
	returns: a dictionary mapping node->{0,1} (0 for periphery, 1 for core)
	"""
	
	A = nx.convert.to_numpy_matrix(graph)	
	
	if partition:
		# convert the dictionary partition into a bit array
		C = numpy.zeroes(len(A))
		for node,value in partition.iteritems():
			C[graph.nodes().index(node)] = int(value)
	else:
		# create a random partition of the graph into core / periphery
		# 0 for periphery, 1 for core
		C = numpy.random.randint(0,2,size=len(A))
		C[0] = 0
		C[1] = 1
		
	C = _kernighanLinOptimizer(A,C,numIterations)
	
	# convert the numpy array to a dictionary
	partition = {}
	for node in graph.nodes():
		partition[node] = C[graph.nodes().index(node)]
	return partition
	
def _kernighanLinOptimizer(A,C,numIterations):
	"""
	Simple optimizer that tries to optimize similarity to the ideal
	core / periphery matrix
	"""
	for t in xrange(numIterations):
		CTentative = C.copy()
		unlockedNodes = range(len(A))
		gk = []
		gkc = []
		runningTotal = 0.0
		while len(unlockedNodes) > 0:
			currentScore = _simpleCorrelationToIdeal(A,CTentative)
			bestScore = _g(A,unlockedNodes[0],CTentative,currentScore)
			bestX = unlockedNodes[0]
			for x in unlockedNodes:
				g = _g(A,x,CTentative,currentScore)
				if g > bestScore: 
					bestScore = g
					bestX = x
			CTentative[bestX] = (CTentative[bestX]+1)%2
			unlockedNodes.remove(bestX)
			runningTotal += bestScore
			gk.append(runningTotal)
			gkc.append(CTentative.copy())
	
		bestScore = max(gk)
		if bestScore > 0:
			bestK = gk.index(max(gk))
			C = gkc[bestK]
	return C

		
def _g(A,a,C,current):
	"""
	calculates the net gain achieved by swapping node a
	from core to periphery or vice versa
	"""
	C[a] = (C[a]+1)%2
	new = _simpleCorrelationToIdeal(A,C)
	C[a] = (C[a]+1)%2
	return new-current

def _simpleCorrelationToIdeal(A,C):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A higher score is better
	
	Not normalized, meaning bigger matrices will tend towards higher scores
	"""
	
	# NOTE: should we include some idea of value/weighted?
	
	a = numpy.repeat(numpy.matrix(C),len(C),axis=0)
	b = numpy.repeat(numpy.matrix(C).transpose(),len(C),axis=1)
	z = a + b
	Cmask = numpy.divide(z,z)
	
	return numpy.multiply(A,Cmask).sum()