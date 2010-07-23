#!nodens-python

# Alex Levenson
# python wrapper for a C++ implementation of the infomap 
# community detection algorithm by Martin Rosvall
# C++ version modified by Alex Levenson to use stdin and stdout
# instead of writing / reading filesystem files

import subprocess
import csv
import StringIO
import networkx as nx
import random

def _findCommunities(graph):
	"""
	Runs the infomap community detection algorithm on graph
	
	graph: a networkx Graph
	
	returns: the raw output from stdout in the form (stdout,stderr)
	"""
	# infomap.cc requires a random seed to be provided
	seed = str(random.randint(1,1000000000))
	
	# convert graph to pajek format
	# have to use a StringIO because networkx only writes pajek to files
	pajekf = StringIO.StringIO()
	nx.write_pajek(graph,pajekf)
	pajekf.seek(0)
	pajekf.readline() # networkx throws an extra line at the top of the file that infomap.cc does not like
	pajek = pajekf.read()
	pajekf.close()
	
	# run the infomap binary and set up std in/out/err piping 
	proc = subprocess.Popen("./infomap/infomap "+seed+" 10",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	
	# send the pajek graph data to the infomap process and retrieve it's response via stdout and stderr 
	com = proc.communicate(pajek) # com[0] is now stdout and com[1] is stderr
	
	# if anything gets written to stderr then there's a problem
	if com[1]:
		raise Exception(com[1])
	return com
	
def writeCommunities(graph,file):
	"""
	Writes a tab delimited file listing the all the nodes in the graph and which communities they belong to
	
	graph: a networkx Graph
	
	path: either a filepath string or a file object to write to
	"""
	
	# nifty networkx utility that returns file if 
	# it's already a file object, and a file object 
	# if it is just a path
	file = nx.utils._get_fh(file, mode='w')
	
	# get the output from infomap.cc
	com = _findCommunities(graph)
	
	# write it
	file.write(com[0])
	file.close

def findCommunities(graph):
	"""
	Runs the infomap community detection algorithm on graph
	
	graph: a networkx Graph
	
	returns: nothing. Each of graph's node's data dictionaries 
	will have an entry "community" that describes which community that node is in
	"""
	
	# get the output from infomap.cc
	com = _findCommunities(graph)
		
	# now use csv.DictReader to parse the tab delimited output in stdout 
	# into a series of dictionaries
	# csv.reader requires a file-like stream so use a StringIO
	stream = StringIO.StringIO(com[0])
	reader = csv.DictReader(stream,delimiter="\t")
	
	# networkx.Graph.node() returns a list, but we need random access to
	# the nodes by name so build a dict indexed by nodes with each node's 
	# 'data' dict for values
	nodesDict = {}
	nodesAndData = graph.nodes(data=True)
	for entry in nodesAndData:
		nodesDict[entry[0]]=entry[1]
		
	# use aforementioned dictionary to fill the community information into
	# each of graph's nodes's 'data' dictiionaries
	for node in reader:
		nodesDict[node["name"]]["community"] = node["module"]