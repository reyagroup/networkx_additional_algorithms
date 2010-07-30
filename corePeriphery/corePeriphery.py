#!nodens-python
# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Thursday July 29th 2010

import random

def _generateRandomPartition(A):
	partition = {}
	for x in xrange(len(A)):
		partition[x] = random.randrange(2)
	return partition
	
def _kernighanLinOptimizer(A,partition=None):
	if not partition:
		partition = _generateRandomPartition(A)
	
	locked = {}
	for x in xrange(len(A)):
		locked[x] = False
	
	currentScore = _simpleCorrelationToIdeal(A,partition)
	
	bestScore = _g(A,0,partition,currentScore)
	bestX = 0
	for x in xrange(1,len(A)):
		if locked[x]: continue
		g = _g(A,x,partition,currentScore)
		print g
		if g > bestScore: 
			bestScore = g
			bestX = x 
	print "Best: " + str(bestScore)

def _g(A,a,partition,current):
	partition[a] = (partition[a]+1)%2
	new = _simpleCorrelationToIdeal(A,partition)
	partition[a] = (partition[a]+1)%2
	return new-current

def _simpleCorrelationToIdeal(A,partition):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A: Adjacency matrix of the graph
	partition: Dictionary mapping node index -> 1 for core and 0 for periphery
	"""
	
	# NOTE: should we include some idea of value/weighted?
	
	p = 0
	size = len(A)
	for i in xrange(size):
		for j in xrange(size):
			if A[i,j] > 0:
				if partition[i] > 0 or partition[j] > 0:
					p+=1
	return p