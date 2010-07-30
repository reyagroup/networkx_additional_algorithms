# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Friday July 23rd 2010

# A python wrapper of the C++ implementation of Martin Rosvall's infomap algorithm for community detection in social networks
# to be used with networkx
# More info at http://www.tp.umu.se/~rosvall, in particular: http://www.tp.umu.se/~rosvall/code.html

# C++ version modified by Alex Levenson to use stdin and stdout
# instead of writing / reading filesystem files

import subprocess
import csv
import StringIO
import networkx as nx
import random
import sys

def _getPathToBinary():
	path = sys.modules[__name__].__file__
	lastSlash = path.rfind("/")
	return path[:lastSlash]+"/infomap-c-impl/infomap"
	
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
	proc = subprocess.Popen(_getPathToBinary()+" "+seed+" 10",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	
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
	
	returns: a dictionary mapping each node --> it's community
	"""
	
	# get the output from infomap.cc
	com = _findCommunities(graph)
		
	# now use csv.DictReader to parse the tab delimited output in stdout 
	# into a series of dictionaries
	# csv.reader requires a file-like stream so use a StringIO
	stream = StringIO.StringIO(com[0])
	reader = csv.DictReader(stream,delimiter="\t")
	
	# build a dictionary mapping node to community and return it
	communities = {}
	for node in reader:
		communities[node["name"]] = node["module"]

	return communities