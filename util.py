"""
Alex Levenson
alex@isnotinvain.com	| www.isnotinvain.com
(c) Reya Group 			| http://www.reyagroup.com
Friday July 23rd 2010
"""

import networkx as nx
import csv
import igraph

def writeDict(dict,file,headerRow=None):
	"""
	Writes dict to file in CSV format
	
	file: a file object or a filepath
	headerRow: a list containing the headers
	"""
	file = nx.utils._get_fh(file, mode='w')

	writer = csv.writer(file)
	if headerRow: writer.writerow(headerRow)
	for k,v in dict.iteritems():
		writer.writerow([k,v])
	file.close()

def writeNestedDict(dict,file,headerRow):
	file = nx.utils._get_fh(file, mode='w')

	writer = csv.writer(file)
	writer.writerow(headerRow)
	for k,d in dict.iteritems():
		row = [k]
		row.extend([d[prop] for prop in headerRow[1:]])
		writer.writerow(row)
	file.close()
	
def writeList(lyst,file,headerRow=None):
	"""
	Writes lyst to file in CSV format

	file: a file object or a filepath
	headerRow: a list containing the headers
	"""
	file = nx.utils._get_fh(file, mode='w')

	writer = csv.writer(file)
	if headerRow: writer.writerow(headerRow)
	for row in lyst:
		writer.writerow(row)
	file.close()
	
def nxToIgraph(graph,directed=None):
	ig = igraph.Graph(directed=directed)
	ig.add_vertices(len(graph)-1)
	ig.add_edges([(g.nodes().index(edge[0]),g.nodes().index(edge[1])) for edge in g.edges()])
	return ig