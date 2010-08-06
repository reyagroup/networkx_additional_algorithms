#!nodens-python
# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Thursday July 29th 2010

import random
import networkx as nx
import numpy

def partition(graph):
	A = nx.convert.to_numpy_matrix(graph)	
	C = _kernighanLinOptimizer(A)
	print  _simpleCorrelationToIdeal(A,C)
	partition = {}
	for node in graph.nodes():
		partition[node] = C[graph.nodes().index(node)]
	return partition
	
def _kernighanLinOptimizer(A,C=None,numIterations=3):
	if not C:
		# create a random partition of the graph into core / periphery
		# 0 for periphery, 1 for core
		C = numpy.random.randint(0,2,size=len(A))
		# need to force one in each
		print _simpleCorrelationToIdeal(A,C)

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
		print  _simpleCorrelationToIdeal(A,C)
	return C

		
def _g(A,a,C,current):
	C[a] = (C[a]+1)%2
	new = _simpleCorrelationToIdeal(A,C)
	C[a] = (C[a]+1)%2
	return new-current

def _simpleCorrelationToIdeal(A,C):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A: Adjacency matrix of the graph
	partition: Dictionary mapping node index -> 1 for core and 0 for periphery
	"""
	
	# NOTE: should we include some idea of value/weighted?
	
	a = numpy.repeat(numpy.matrix(C),len(C),axis=0)
	b = numpy.repeat(numpy.matrix(C).transpose(),len(C),axis=1)
	z = a + b
	Cmask = numpy.divide(z,z)
	
	return numpy.multiply(A,Cmask).sum()