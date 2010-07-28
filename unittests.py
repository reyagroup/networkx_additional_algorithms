#!nodens-python
import unittest
import constraint
import networkx as nx
import cPickle

class TestSequenceFunctions(unittest.TestCase):

	def assertWithin(self,x,y,e):
		"""
		Ensure x is within e of y
		"""
		
		self.assertTrue(abs(x-y)<e)
		
	def setUp(self):
		self.undirected = nx.read_edgelist("adp.edgelist",create_using=nx.Graph())
		f = open("adp_constraints.pickle","r")
		self.undirectedExpected = cPickle.load(f)

	def test_undirected_constraints(self):
		constraints = constraint.calcConstraints(self.undirected,False,True,True)
		
		for node in constraints:
			for entry in constraints[node]:
				self.assertWithin(constraints[node][entry],self.undirectedExpected[node][entry],0.000000001)

if __name__ == '__main__':
	unittest.main()
