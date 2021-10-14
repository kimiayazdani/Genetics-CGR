import requests
import re

def get_ref_genome(pos1, pos2):
	url = 'http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=chr19:' + str(pos1+ 1) + ',' + str(pos2 + 1)
	header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	data = requests.get(url,headers=header)
	reference_genome = re.split('<|>',data.text)[10]
	reference_genome = reference_genome.replace('\n','').upper()
	return reference_genome

if __name__ == "__main__":
	# Script purpose: recreate the sequences, only taking mutations into account (w.o indel)
	gene1 = (10216899, 10225456)
	gene2 = (14063304, 14072254)
	ref_gen = get_ref_genome(*gene1) + get_ref_genome(*gene2)
	# print(ref_gen[:500], len(ref_gen))

