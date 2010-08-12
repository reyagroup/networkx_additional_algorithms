# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Tuesday August 10th 2010

# A generic genetic optimizer

import random
from math import ceil

class GeneticOptimizer(object):
	"""
	A generic genetic optimizer
	Based on code found in Toby Segaran's book Collective Intelligence
	"""	
	def __init__(self,populationSize,survivalRate,maxGenerations,mutateVsBreedRate=0.5,quitAfterStable=0.1):
		"""
		populationSize: the size of each generation's population. This is the number of solutions to be 
			explored each round. This has a large effect on execution time, but the higher the better the results will be.
		
		survivalRate: percentage of population that moves on to the next generation to breed and mutate into the new population
		
		maxGenerations: number of generations to run, directly effects execution time and result quality (higher is better)
			however, if quitAfterStable is set then the algorithm may quit earlier than maxGenerations specifies
		
		mutateVsBreedRate: ratio of mutate:breed. Used to decide whether to mutate dna or to breed dna.
		
		quitAfterStable: set to False if you want exactly maxGenerations number of generations. Otherwise,
			if (quitAfterStable * populationSize) number of generations yield the same result, the algorithm will
			terminate
		"""
		self.populationSize = populationSize
		self.survivalRate = survivalRate
		self.maxGenerations = maxGenerations
		self.mutateVsBreedRate = mutateVsBreedRate
		self.quitAfterStable = quitAfterStable
			
	def optimize(self):
		"""
		Runs the genetic optimizer
		"""
		population = self.generateInitialPopulation()
		
		topElite = int(self.survivalRate * self.populationSize) # how many dna survive to the next round
		
		# keep track of how many generations in a row have yielded the same result
		if self.quitAfterStable:
			numMatches = 0
			previousScore = None
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
			
			# if the user want's to keep tabs on each generation
			self.statusReport(g,scores)
			
			# if there have not been any improvements in a long time, return the best score
			# and call it good enough (if quitAfterStable is enabled)
			if self.quitAfterStable:
				if previousScore:
					if previousScore==scores[0][0]:
						numMatches += 1
					else:
						numMatches = 0
				previousScore = scores[0][0]				
				if numMatches >= numTrailingScores: return scores[0][1]
				
		return scores[0][1]

	def statusReport(self,g,population):
		"""
		This will be called a the end of creating each new generation
		You can override this to inspect the progress as the algorithm progresses
		or to print out the score at each iteration
		
		Defaults to doing nothing
		
		g: the number of the generation
		
		population: the current population as a list of (score,dna) pairs in sort order by best score
			so population[0][0] is the best score so far and population[0][1] is the best solution so far
			
		"""
		pass
					
	def generateInitialPopulation(self):
		"""
		Returns the initial population as a list of dna (possible solutions to be evaluated)
		This is usually a randomly generated list of dna
		This should be of size self.populationSize
		"""
		raise NotImplementedError("Must implement a population generator")

	def mutate(self,dna):
		"""
		given dna, return a somehow 'mutated' version of dna
		It should be a small change from the original
		"""
		raise NotImplementedError("Must implement a dna mutator")

	def breed(self,dna1,dna2):
		"""
		given dna1 and dna2, return the offspring of the two
		It should be a dna that takes roughly equal (or on average roughly equal)
		components from dna1 and dna2 and combines them together into a new
		possible solution
		"""
		raise NotImplementedError("Must implement a dna breeder")

	def getScore(self,dna):
		"""
		given dna, return a score representing how "good" this solution is
		Higher score means a better solution (this is important, the optimzer tries to MAXIMIZE this value)
		"""
		raise NotImplementedError("Must implement a dna scorer")