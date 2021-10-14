from pysam import VariantFile
import pysam
import numpy as np


def load_data_from():
	f = open("./DataPop/asian.txt", 'r')
	f = open("./DataPop/euro.txt", 'r')

	for line in f:
		print(line)

def vcf_with_pysam():
	bcf_in = VariantFile("./DataPop/ALL.chr19.phase3_integrated.20130502.genotypes.bcf")
	print(list(bcf_in.header.info))
	i = 0
	for rec in bcf_in.fetch():
		print(i, rec.pos, rec.format.keys(), rec.info.keys(),rec.ref, rec.qual, rec.alts, list(rec.samples)[:5])
		print(dict(rec.samples['HG00096']))
		if 'SVTYPE' in rec.info:
			print(i, rec.info['SVTYPE'])

		# if rec.alts[1]:
			# print(i, rec.pos, rec.format.keys(), rec.info.keys(),rec.ref, rec.qual, rec.alts)

		i += 1
		if i == 100:
			break




	# print(bcf_in.header)
	




if __name__ == "__main__":
	# vcf_with_pysam()
	load_data_from()