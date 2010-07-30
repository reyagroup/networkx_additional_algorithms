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
	
