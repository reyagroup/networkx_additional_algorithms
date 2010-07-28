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

	def test_undirected_constraints_whole(self):
		f = open("adp_constraints_whole.pickle","r")
		expected = cPickle.load(f)
		f.close()
		
		constraints = constraint.calcConstraints(self.undirected,False,True,True)
		
		for node in constraints:
			for entry in constraints[node]:
				self.assertWithin(constraints[node][entry],expected[node][entry],0.000000001)
				
	def test_undirected_constraints_ego(self):
		f = open("adp_constraints_ego.pickle","r")
		expected = cPickle.load(f)
		f.close()

		constraints = constraint.calcConstraints(self.undirected,False,True,True)

		for node in constraints:
			for entry in constraints[node]:
				self.assertWithin(constraints[node][entry],expected[node][entry],0.000000001)

if __name__ == '__main__':
	unittest.main()
