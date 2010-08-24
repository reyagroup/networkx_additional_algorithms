"""
Alex Levenson
alex@isnotinvain.com	| www.isnotinvain.com
(c) Reya Group 			| http://www.reyagroup.com
Friday July 23rd 2010

Calculates brokerage roles, as described by Steven Borgatti in http://www.analytictech.com/essex/Lectures/Brokerage.pdf
"""

import networkx as nx
import itertools

class _RoleClassifier(object):
	roleTypes = { \
				 "coordinator"		: lambda pred,broker,succ: pred == broker == succ, \
				 "gatekeeper" 	 	: lambda pred,broker,succ: pred != broker == succ, \
				 "representative"	: lambda pred,broker,succ: pred == broker != succ, \
				 "consultant"		: lambda pred,broker,succ: pred == succ != broker, \
				 "liaison"			: lambda pred,broker,succ: pred != succ and pred != broker and broker != succ, \
				}
				
	@classmethod
	def classify(cls,predecessor_group,broker_group,successor_group):
		for role,predicate in cls.roleTypes.iteritems():
			if predicate(predecessor_group,broker_group,successor_group):
				return role
		raise Exception("Could not classify... this should never happen")
	
def getBrokerageRoles(graph,partition):
	"""
	Counts how many times each node in graph acts as one of the five brokerage roles described by Steven Borgatti in
	http://www.analytictech.com/essex/Lectures/Brokerage.pdf
	
	graph: a networx DiGraph
	partition: a dictionary mapping node -> group, must map every node. If a node has no group associate then put it by itself in a new group
	
	returns: {node -> {"cooridnator": n, "gatekeeper": n, "representative": n, "consultant": n, "liaison": n}} where n is the number of times
	node acted as that role
	"""
	
	roleClassifier = _RoleClassifier()
	
	roles = dict((node, dict((role,0) for role in roleClassifier.roleTypes)) for node in graph)
	
	for node in graph:
		for successor in graph.successors(node):
			for predecessor in graph.predecessors(node):
				if successor == predecessor or successor == node or predecessor == node: continue
				if not (graph.has_edge(predecessor, successor)):
					# found a broker!
					# now which kind depends on who is in which group
					roles[node][roleClassifier.classify(partition[predecessor],partition[node],partition[successor])] += 1
	return roles
						