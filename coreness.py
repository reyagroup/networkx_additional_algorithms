"""
Alex Levenson
alex@isnotinvain.com	| www.isnotinvain.com
(c) Reya Group 			| http://www.reyagroup.com
Friday July 23rd 2010
"""

from scipy import optimize
from scipy.stats.stats import pearsonr
import numpy
import networkx as nx

def coreCorrelation(A,C):
	"""
	returns the pearson correlation between A and
	the ideal coreness matrix created from C
	
	A: ajacency matrix (valued or unvalued)
	C: 1D matrix representing the coreness of each node
	"""
	cMat = numpy.matrix(C)
	Cij = numpy.multiply(cMat,cMat.transpose())
	return pearsonr(A.flat,Cij.flat)
	
def _coreFitness(C,*args):
	"""
	converts coreCorrelation(A,C) to something useable
	with scipy.optimize (which aims to MINIMIZE a function)
	Need to express highest positive correlation as function
	to be minimized
	"""
	return coreCorrelation(args[0],C)[0] * -1.0

def getCoreness(graph):
	"""
	Calculates each node's 'coreness'
	returns: a dictionary mapping node->coreness, the final correlation to the ideal core/periphery model
	"""
	A = nx.convert.to_numpy_matrix(graph)
	initialC = numpy.random.rand(len(A)) # can we do better? Is it important? Maybe use constraint or centrality? 
	best = optimize.fmin_l_bfgs_b(_coreFitness, initialC,args=(A,None),approx_grad=True,bounds=[(0.0,1.0) for i in xrange(len(A))])
	print best
	
	part = {}
	for node in graph:
		part[node] = best[0][graph.nodes().index(node)]
	
	return part,best[1] * -1.0