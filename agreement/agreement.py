# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Friday July 30th 2010

def tanimoto(a,b):
	"""
	returns the similarity between sets a and b
	"""
	c = [v for v in a if v in b]
	return float(len(c))/(len(a)+len(b)-len(c))

def printSummary(trials):
	for t1 in xrange(len(trials)):
		for t2 in xrange(t1+1,len(trials)):
			for com1 in trials[t1].values():
				sims = []
				for com2 in trials[t2].values():
					similarity = tanimoto(com1,com2)
					sims.append(similarity)
			if max(sims) < 0.99999999999:
				print "could not find a match for: " + str(com1) + str(max(sims))

def electRep(lyst):
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

def addByRep(superclasses,cet,threshold):
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
		newRep = electRep(bestEntry[1])
		bestEntry[0] = newRep
	else:
		superclasses.append([cet,[cet]])

def findAgreementIn(trials,setSimilarityThreshold=0.8,voteThreshold=0.8):
	superclasses = []
	for trial in trials:
		for cet in trial.values():
			addByRep(superclasses,cet,setSimilarityThreshold)

	histogram = map(lambda x: (x[0],len(x[1])),superclasses)
	histogram.sort(lambda x,y: y[1]-x[1])
	
	l = float(len(trials))
	for cet in xrange(len(histogram)):
		if (histogram[cet][1] / l) < voteThreshold: break
	
	del histogram[cet:]
	return map(lambda x: x[0],histogram)