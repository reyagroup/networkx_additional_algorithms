"""
Alex Levenson
alex@isnotinvain.com	| www.isnotinvain.com
(c) Reya Group 			| http://www.reyagroup.com
Friday July 23rd 2010

Usefull methods for finding set similarity, entries that best represent a list, and agreement between multiple "trials"
"""

def tanimoto(a,b):
	"""
	returns the similarity between sets a and b,
	between 0 and 1
	"""
	c = [v for v in a if v in b]
	return float(len(c))/(len(a)+len(b)-len(c))

def getBestRepresentative(lyst):
	"""
	returns the element that 'best represents' lyst as a whole,
	meaning the element with maximum tanimoto between itself and
	all other elements in lyst
	"""
	bestScore = 0.0
	bestCandidate = None
	for candidate in lyst:
		score = 0.0
		for cet in lyst:
			if cet is candidate: continue
			score += tanimoto(candidate,cet)
		if score > bestScore:
			bestScore = score
			bestCandidate = candidate
	return bestCandidate

def _classify(superclasses,cet,threshold):
	"""
	Places cet into superclasses by choosing which superclass cet best fits into
	If cet does not fit into any superclass within the given threshold, cet is deemed
	ad new superclass and added to superclasses as such
	"""
	best = 0.0
	bestEntry = None
	for entry in superclasses:
		rep,lyst = entry
		score = tanimoto(rep,cet)
		if score > best:
			best = score
			bestEntry = entry
	if best > threshold:
		bestEntry[1].append(cet)
		newRep = getBestRepresentative(bestEntry[1])
		bestEntry[0] = newRep
	else:
		superclasses.append([cet,[cet]])

def findAgreementBetween(trials,setSimilarityThreshold=0.8,voteThreshold=0.8,returnFullHistogram=False):
	"""
	Finds 'agreement' amongst a series of 'trials'
	More specifically, given:
	
		trials: a list of lists of sets, each list of sets representing a single trial

		setSimilarityThreshold: The tanimoto score required to consider two sets 'close enough to equal' or in the same 'super-class'

		voteThreshold: The percentage of trials that must 'agree' for a set to be considered a member of the return value
	
	returns a list of sets which voteThreshold percent of the trials contained, or rather contained within setSimililarityThreshold
	
	A 'representative' will be chosen for each super-class, and it will be the set that is present in the return value.
	It is the one which has the highest similarity to all the other sets in it's super-class
	
	if returnFullHistogram is set to True, then voteThreshold will be ignored and a list of tuples will be returned
	in the form, for every super-class, (super-class representative, number of sets in this super-class)
	"""
	superclasses = []
	for trial in trials:
		for cet in trial:
			_classify(superclasses,cet,setSimilarityThreshold)

	histogram = map(lambda x: (x[0],len(x[1])),superclasses)
	histogram.sort(lambda x,y: y[1]-x[1])
	
	if not returnFullHistogram:
		l = float(len(trials))
		for cet in xrange(len(histogram)):
			if (histogram[cet][1] / l) < voteThreshold: break
		del histogram[cet:]
		return map(lambda x: x[0],histogram)
	
	return histogram