# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Tuesday August 10th 2010

# A generic genetic optimizer

import random
from math import ceil

class GeneticOptimizer(object):
	
	def __init__(self,populationSize,survivalRate,maxGenerations,mutateVsBreedRate=0.5,quitAfterStable=0.1):
		self.populationSize = populationSize
		self.survivalRate = survivalRate
		self.maxGenerations = maxGenerations
		self.mutateVsBreedRate = mutateVsBreedRate
		self.quitAfterStable = quitAfterStable
			
	def optimize(self):
		topElite = int(self.survivalRate * self.populationSize)
		population = self.generateInitialPopulation()
		if self.quitAfterStable:
			trailingScores = []
			numTrailingScores = int(self.quitAfterStable * self.populationSize)
		for g in xrange(self.maxGenerations):
			scores = [(self.getScore(dna),dna) for dna in population]
			scores.sort(lambda x,y: int(ceil(y[0]-x[0])))
			ranked = [v for (s,v) in scores]
			population = ranked[:topElite]
			while len(population) < self.populationSize:
				if random.random() < self.mutateVsBreedRate:
					c = random.randint(0,topElite)
					population.append(self.mutate(ranked[c]))
				else:
					c1 = random.randint(0,topElite)
					c2 = random.randint(0,topElite)
					population.append(self.breed(ranked[c1],ranked[c2]))
			
			if self.quitAfterStable:
				trailingScores.append(scores[0][0])
				trailingScores = trailingScores[-numTrailingScores:]
				eq = [v for v in trailingScores if v==trailingScores[0]]
				if len(eq) == numTrailingScores:
					return scores[0][1]
				
			self.statusReport(g,scores[0][0])
		return scores[0][1]

	def statusReport(self,g,score):
		pass
					
	def generateInitialPopulation(self):
		raise NotImplementedError("Must implement a population generator")

	def mutate(self,dna):
		raise NotImplementedError("Must implement a dna mutator")

	def breed(self,dna1,dna2):
		raise NotImplementedError("Must implement a dna breeder")

	def getScore(self,dna):
		raise NotImplementedError("Must implement a dna scorer")