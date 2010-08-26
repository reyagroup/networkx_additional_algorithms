#!nodens-python
#!/usr/bin/python
"""
Alex Levenson
alex@isnotinvain.com	| www.isnotinvain.com
(c) Reya Group 			| http://www.reyagroup.com
Friday July 23rd 2010
"""

import unittest
import networkx as nx
import agreement
import constraint
import coreness
import brokerage
import cPickle
import itertools
from scipy.stats.stats import pearsonr

class TestAdditionalAlgorithms(unittest.TestCase):
		
	def setUp(self):
		self.directed = nx.read_edgelist("unit_test_data/bkoff_unweighted.edgelist",create_using=nx.DiGraph())
		self.undirected = nx.Graph(self.directed)
		self.partition = {"1":1,"2":1,"3":1,"4":1,"5":1,"6":1,"7":1,"8":1,"9":1,"10":1,"11":2,"12":2,"13":2,"14":2,"15":2,"16":2,"17":2,"18":2,"19":3,"20":3,"21":3,"22":3,"23":4,"24":4,"25":4,"26":4,"27":4,"28":4,"29":4,"30":4,"31":4,"32":4,"33":5,"34":5,"35":5,"36":6,"37":7,"38":8,"39":9,"40":9}
		self.graphs = {"undirected": self.undirected, "directed": self.directed}

	def test_brokerage(self):
		roles = brokerage.getBrokerageRoles(self.directed,self.partition)
		f = open("unit_test_data/bkoff_brokerage.pickle","r")
		shouldBe = cPickle.load(f)
		f.close()
		self.assertEqual(roles,shouldBe)
	
	def test_constraint(self):
		runs = {(True,True,True) : None,		# in / out links, whole network
				(True,True,False) : None,  	# in / out links, ego network
				(True,False,False) : None, 	# in links only, ego network
				(False,True,False) : None 	# out links only, ego network
				}
				
		f = open("unit_test_data/bkoff_structural_holes_inlinks_outlinks_wholenet.pickle","r")
		runs[(True,True,True)] = cPickle.load(f)
		f.close()
		f = open("unit_test_data/bkoff_structural_holes_inlinks_outlinks_egonet.pickle","r")
		runs[(True,True,False)] = cPickle.load(f)
		f.close()
		f = open("unit_test_data/bkoff_structural_holes_inlinks_egonet.pickle","r")
		runs[(True,False,False)] = cPickle.load(f)
		f.close()
		f = open("unit_test_data/bkoff_structural_holes_outlinks_egonet.pickle","r")
		runs[(False,True,False)] = cPickle.load(f)
		f.close()
		
		for type,graph in self.graphs.iteritems():
			for params,shouldBe in runs.iteritems():
				msg = "Incorrect calculation of constraint for graph type: " + type + " with parameters: " + str(params)
				constraints = constraint.getConstraints(graph,*params)
				# currently only checking cIndex
				cIndexes = dict((n,c["C-Index"]) for n,c in constraints.iteritems())
				for k,v in cIndexes.iteritems():
					self.assertAlmostEqual(v,shouldBe[k], msg=msg)

	def test_coreness(self):
		f = open("unit_test_data/bkoff_coreness.pickle","r")
		shouldBe = cPickle.load(f)
		shouldBe = [shouldBe[i] for i in sorted(shouldBe.keys())]
		f.close()
		
		cness = coreness.getCoreness(self.directed)
		cness = [cness[i] for i in sorted(cness.keys())]
		r = pearsonr(cness,shouldBe)[0]
		msg = "Correlation between calculated coreness and correct coreness is too low (" + str(r) + ")"
		self.assert_(r>0.99,msg=msg)
		
		
if __name__ == '__main__':
	unittest.main()