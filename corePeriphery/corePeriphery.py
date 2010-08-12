# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Thursday July 29th 2010

# simple discrete core periphery partitioner, based on the paper:
# Computing Core/Periphery Structures and Permutation Tests for Social Relations Data
#                                        by
#               John P. Boyd, William J. Fitzgerald, and Robert J. Beck
#                  University of California at Irvine, CA 92697, USA


import random
import networkx as nx
import numpy
from geneticOptimizer import *

class CorePeripheryOptimizer(GeneticOptimizer):
	def __init__(self,A,populationSize,survivalRate,maxGenerations,mutateVsBreedRate):
		GeneticOptimizer.__init__(self,populationSize,survivalRate,maxGenerations,mutateVsBreedRate)
		self.A = A
		
	def generateInitialPopulation(self):
		return [numpy.random.randint(0,2,size=len(self.A)) for i in xrange(self.populationSize)]
		
	def mutate(self,dna):
		i = random.randint(0,len(dna)-1)
		m = dna.copy()
		m[i] = (m[i] + 1)%2
		return m
		
	def breed(self,dna1,dna2):
		l = min(map(len,[dna1,dna2])) 
		mask = [random.randint(0,1) for i in xrange(l)]
		src = (dna1,dna2)
		child = numpy.empty_like(dna1)
		for i in xrange(l):
			child[i] = src[mask[i]][i]
		return child
		
	def getScore(self,dna):
		#return _simpleCorrelationToIdeal(self.A,dna)
		return _betterCorrelation(self.A,dna)
		
	def statusReport(self,g,score):
		print (g,score)

def partition(graph,populationSize=100,survivalRate=0.75,maxGenerations=100,mutateVsBreedRate=0.5):
	"""
	Partitions graph into a core set and a periphery set
	using a genetic optimizer
	
	graph: a networkx graph
	populationSize, survivalRate,maxGenerations,mutateVsBreedRate: see geneticOptimizer.py
	
	returns: a dictionary mapping node->{0,1} (0 for periphery, 1 for core)
	"""
	
	A = nx.convert.to_numpy_matrix(graph)
	opt = CorePeripheryOptimizer(A,populationSize,survivalRate,maxGenerations,mutateVsBreedRate)
	best = opt.optimize()

	# convert the numpy array to a dictionary
	partition = {}
	for node in graph.nodes():
		partition[node] = best[graph.nodes().index(node)]
	return partition
	
def naiveOptimizer(graph,steps=10000):
	"""
	Partitions graph into a core set and a periphery set
	using the worst optimizer (random explorer). All other methods should outperform this one.
	
	graph: a networkx graph
	steps: how many solutions to explore
	
	returns: a dictionary mapping node->{0,1} (0 for periphery, 1 for core)
	"""
	A = nx.convert.to_numpy_matrix(graph)	

	best = numpy.random.randint(0,2,size=len(A))
	bestScore = _betterCorrelation(A,best)
	for t in xrange(steps):
		bitPartition = numpy.random.randint(0,2,size=len(A))
		score = _betterCorrelation(A,bitPartition)
		if score > bestScore:
			bestScore = score
			best = bitPartition.copy()

	# convert the numpy array to a dictionary
	partition = {}
	for node in graph.nodes():
		partition[node] = best[graph.nodes().index(node)]
	return partition
	
def _betterCorrelation(A,bitPartition):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A higher score is better
	
	Not normalized, meaning bigger matrices will tend towards higher scores (I think)
	"""
	a = numpy.repeat(numpy.matrix(bitPartition),len(bitPartition),axis=0)
	b = numpy.repeat(numpy.matrix(bitPartition).transpose(),len(bitPartition),axis=1)
	core_core_mask = numpy.bitwise_and(a,b)
	periph_periph_mask = numpy.bitwise_and((a+1)%2,(b+1)%2)

	diff = numpy.multiply(A,core_core_mask)
	diff = diff - core_core_mask
	diff = numpy.multiply(diff,diff)
	lostPoints = diff.sum()	
	
	
	diff = numpy.multiply(A,periph_periph_mask)
	lostPoints += diff.sum()

	return len(a)**2 - lostPoints
	
def _simpleCorrelation(A,bitPartition):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A higher score is better
	
	Not normalized, meaning bigger matrices will tend towards higher scores (I think)
	"""
	a = numpy.repeat(numpy.matrix(bitPartition),len(bitPartition),axis=0)
	b = numpy.repeat(numpy.matrix(bitPartition).transpose(),len(bitPartition),axis=1)
	involves_core_mask = numpy.bitwise_or(a,b)
	diff = A - involves_core_mask
	diff = numpy.multiply(diff,diff)
	return len(A)**2 - (diff.sum())	