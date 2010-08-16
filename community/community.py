# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Monday August 16th

from infomap import findBestPartition
from ..agreement import findAgreementBetween

def repeatedInfomap(graph,numTrials=10,setSimilarityThreshold=0.8,voteThreshold=0.8,returnFullHistogram=False):
	"""
	runs the infomap community detection algorithm numTrials times, and returns the "agreement" between the runs
	
	graph: a networkx graph

	numTrials: number of runs of the infomap algorithm

	setSimilarityThreshold,voteThreshold: see findAgreementBetween
	
	returns a dictionary mapping node->[list of communities node belongs to]
	if returnFullHistogram is set to True, then voteThreshold will be ignored and a list of tuples will be returned
	in the form, for every community, (community representative, number of trials that 'voted' for this community)
	
	A 'representative' will be chosen for each community, and it will be the set that is present in the return value.
	It is the one which has the highest similarity to all the other sets in it's super-class
	"""
	runs = [findBestPartition(graph,partitionOnly=False) for t in xrange(numTrials)]
	trials = [c[1].values() for c in runs]
	
	agree = findAgreementBetween(trials,setSimilarityThreshold=setSimilarityThreshold,voteThreshold=voteThreshold,returnFullHistogram=returnFullHistogram)
	
	if returnFullHistogram:
		return agree
	
	partition = {}
	for cet in xrange(len(agree)):
		for node in agree[cet]:
			if node not in partition:
				partition[node] = []
			partition[node].append(cet)
			
	return partition