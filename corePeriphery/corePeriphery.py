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
		bitPartition = numpy.zeroes(len(A))
		for node,value in partition.iteritems():
			bitPartition[graph.nodes().index(node)] = int(value)
	else:
		# create a random partition of the graph into core / periphery
		# 0 for periphery, 1 for core
		bitPartition = numpy.random.randint(0,2,size=len(A))
		# force at least one in each partition
		bitPartition[0] = 0
		bitPartition[1] = 1
		
	bitPartition = _kernighanLinOptimizer(A,bitPartition,numIterations)
	
	# convert the numpy array to a dictionary
	partition = {}
	for node in graph.nodes():
		partition[node] = bitPartition[graph.nodes().index(node)]
	return partition
	
def _kernighanLinOptimizer(A,bitPartition,numIterations):
	"""
	Simple optimizer that tries to optimize similarity to the ideal
	core / periphery matrix
	"""
	for t in xrange(numIterations):
		# need a place to store tentative swaps
		tentativePartition = bitPartition.copy()
		
		# set all nodes to unlocked
		unlockedNodes = range(len(A))
		
		# gains[i] holds the net gain for applying swaps 0 through i
		gains = []
		cumulativeGain = 0
		
		# tentativePartitions[i] holds the partion after swaps 0 through i have been applied
		# TODO: quite memory inefficient... is there a better way to do this? (yes there is)
		tentativePartitions = []
		
		# swap each node from it's current partition, in order of
		# best net gain, keeping track of net gain as we go
		while len(unlockedNodes) > 0:
			
			# find the best node left to swap
			currentScore = _simpleCorrelationToIdeal(A,tentativePartition)
			bestGain = _gainDelta(A,unlockedNodes[0],tentativePartition,currentScore)
			bestNode = unlockedNodes[0]			
			for n in unlockedNodes:
				gain = _gainDelta(A,n,tentativePartition,currentScore)
				if gain > bestGain: 
					bestGain = gain
					bestNode = n
			
			# best node to swap found, perform the swap
			tentativePartition[bestNode] = (tentativePartition[bestNode]+1)%2
			unlockedNodes.remove(bestNode)
			
			# keep track of cumulativeGain thus far and save the current tentative
			cumulativeGain += bestGain
			gains.append(cumulativeGain)
			tentativePartitions.append(tentativePartition.copy())
	
		# Now swaps 0...K...len(A) have been performed,
		# now we need to find K, such that the sum of the gains
		# from swaps 0...K is highest 
		bestGain = max(gains)
		
		if bestGain > 0:
			# Make the tentative swaps from 0 to K permanent swaps
			bestK = gains.index(max(gains))
			bitPartition = tentativePartitions[bestK]
		else:
			# if bestGain is negative then we're not going
			# to find anything better using this algorithm
			return bitPartition

	return bitPartition

		
def _gainDelta(A,a,bitPartition,current):
	"""
	calculates the net gain achieved by swapping node a
	from core to periphery or vice versa
	"""
	bitPartition[a] = (bitPartition[a]+1)%2
	new = _simpleCorrelationToIdeal(A,bitPartition)
	bitPartition[a] = (bitPartition[a]+1)%2
	return new-current

def _simpleCorrelationToIdeal(A,bitPartition):
	"""
	Calculates how close to ideal A is in terms of
	being a core / periphery structure
	
	A higher score is better
	
	Not normalized, meaning bigger matrices will tend towards higher scores
	"""
	
	# NOTE: should we include some idea of value/weighted?
	
	a = numpy.repeat(numpy.matrix(bitPartition),len(bitPartition),axis=0)
	b = numpy.repeat(numpy.matrix(bitPartition).transpose(),len(bitPartition),axis=1)
	z = a + b
	bitPartitionmask = numpy.divide(z,z)
	
	return numpy.multiply(A,bitPartitionmask).sum()