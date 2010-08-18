# Alex Levenson
# nosnevelxela@gmail.com
# Reya Group
# Wednesday August 18th 2010

import networkx as nx

def writeDict(dict,file,headerRow=None):
	"""
	Writes dict to file in CSV format
	
	file: a file object or a filepath
	headerRow: a list containing the headers
	"""
	file = nx.utils._get_fh(file, mode='w')

	writer = csv.writer(file)
	if headerRow: writer.writerow(headerRow)
	for k,v in dict:
		writer.writerow([k,v])
	file.close()