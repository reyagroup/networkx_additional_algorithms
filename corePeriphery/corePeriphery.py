# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Thursday July 29th 2010

# simple discrete core peripher_correlationLessStricty partitioner, based on the paper:
# Computing Core/Periphery Structures and Permutation Tests for Social Relations Data
#                                        by
#               John P. Boyd, William J. Fitzgerald, and Robert J. Beck
#                  University of California at Irvine, CA 92697, USA


import random
import networkx as nx
import numpy
from geneticOptimizer import *

# need to fill in the implementation details for the generic optimizer
# see GeneticOptimizer for details
class CorePeripheryOptimizer(GeneticOptimizer):
	def __init__(self,A,populationSize,survivalRate,maxGenerations,mutateVsBreedRate,quitAfterStable,correlationMode):
		GeneticOptimizer.__init__(self,populationSize,survivalRate,maxGenerations,mutateVsBreedRate,quitAfterStable)
		self.A = A
		self.correlationMode = correlationMode
		
	def generateInitialPopulation(self):
		return [numpy.random.randint(0,2,size=len(self.A)) for i in xrange(self.populationSize)]
		
	def mutate(self,dna):
		# swap one node from core to perip or vice versa
		i = random.randint(0,len(dna)-1)
		m = dna.copy()
		m[i] = (m[i] + 1)%2
		return m
		
	def breed(self,dna1,dna2):
		# for each node in dna1 and dna2,
		# randomly choose which parent to take
		# each node from
		if len(dna1) > len(dna2):
			dna1,dna2 = dna2,dna1
		
		src = (dna1,dna2)
		child = numpy.empty_like(dna1)
		for i in xrange(len(dna1)):
			child[i] = src[random.randint(0,1)][i]
		for i in xrange(len(dna2)-len(dna1)):
			child[i+len(dna1)] = dna2[i+len(dna1)]
		return child
				
	def getScore(self,dna):
		return _correlationToIdeal(self.A,dna,self.correlationMode)
		
	def statusReport(self,g,scores):
		print (g,scores[0][0])

def _correlationToIdeal(A,bitPartition,mode):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A higher score is better
	
	A: adjacency matrix of the graph
	bitPartition: array of 1s and 0s representing the partition of nodes into core / periphery
	
	core_core: weight for core to core connections
	core_periphery: weight for core to periphery and periphery to core connections
	periphery_periphery: weight for periphery to periphery connections
	
	positive weights mean this connection type is good, negative weights mean this connect type is bad,
	and zero weights mean ignore this type of connection
	
	Not normalized
	"""
	a = numpy.repeat(numpy.matrix(bitPartition),len(bitPartition),axis=0)
	b = numpy.repeat(numpy.matrix(bitPartition).transpose(),len(bitPartition),axis=1)
	core_core_mask = numpy.bitwise_and(a,b)
	core_periph_mask = numpy.bitwise_xor(a,b)
	periph_periph_mask = numpy.bitwise_or(a,b)
	periph_periph_mask = (periph_periph_mask+1)%2
	
	masks_and_weights = ((core_core_mask,mode[0]), \
						(core_periph_mask,mode[1]), \
						(periph_periph_mask,mode[2]))
	score = 0
	for mask,weight in masks_and_weights:
		if weight == 0:
			continue
		elif weight > 0:
			# we're looking for ones within the mask region
			score += numpy.multiply(A,mask).sum()
		else:
			# we're looking for zeros within the mask region
			# mask.sum() is the number of zeroes there could be
			# so we just subtract the number of ones that were found
			score += mask.sum() - numpy.multiply(A,mask).sum()
	return score
	
def partition(graph,populationSize=100,survivalRate=0.75,maxGenerations=100,mutateVsBreedRate=0.5,quitAfterStable=0.1,core_core=1,core_periphery=0,periphery_periphery=-1):
	"""
	Partitions graph into a core set and a periphery set
	using a genetic optimizer
	
	graph: a networkx graph
	populationSize, survivalRate,maxGenerations,mutateVsBreedRate: see geneticOptimizer.py
	
	returns: a dictionary mapping node->{0,1} (0 for periphery, 1 for core)
	"""
	
	A = nx.convert.to_numpy_matrix(graph)
	opt = CorePeripheryOptimizer(A,populationSize,survivalRate,maxGenerations,mutateVsBreedRate,quitAfterStable,(core_core,core_periphery,periphery_periphery))
	best = opt.optimize()

	# convert the numpy array to a dictionary
	partition = {}
	for node in graph.nodes():
		partition[node] = best[graph.nodes().index(node)]
	return partition
	
def naiveOptimizer(graph,steps=10000,correlationFunction=_correlationToIdeal):
	"""
	Partitions graph into a core set and a periphery set
	using the worst optimizer (random explorer). All other methods should outperform this one.
	
	graph: a networkx graph
	steps: how many solutions to explore
	
	returns: a dictionary mapping node->{0,1} (0 for periphery, 1 for core)
	"""
	A = nx.convert.to_numpy_matrix(graph)	

	best = numpy.random.randint(0,2,size=len(A))
	bestScore = correlationFunction(A,best)
	for t in xrange(steps):
		bitPartition = numpy.random.randint(0,2,size=len(A))
		score = correlationFunction(A,bitPartition)
		if score > bestScore:
			bestScore = score
			best = bitPartition.copy()

	# convert the numpy array to a dictionary
	partition = {}
	for node in graph.nodes():
		partition[node] = best[graph.nodes().index(node)]
	return partition