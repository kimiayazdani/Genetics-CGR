from pysam import VariantFile
import pysam
import numpy as np
import glob
import pandas as pd
import vcf
import gzip
from pprint import pprint

def load_data_from(asia=True):
	samples = list()
	asian_path, euro_path = glob.glob('./DataPop/AsianFastas/*t.fa'), glob.glob('./DataPop/EuroFastas/*t.fa')
	right_path = asian_path if asia else euro_path
	for f in right_path:
		samples.append(f[-14:-7])

	return samples


def process_data(df):
	print(df.shape)
	only_snp = df[df.var_type=='snp']
	sample_GT = only_snp[df.columns[7:]]
	sample_GT['SUM'] = sample_GT.sum(axis=1)
	

def vcf_with_pysam():
	bcf_in = VariantFile("./DataPop/ALL.chr19.phase3_integrated.20130502.genotypes.bcf")
	print(list(bcf_in.header.info))
	i = 0
	for rec in bcf_in.fetch():
		print(i, rec.pos, rec.format.keys(), rec.info.keys(),rec.ref, rec.qual, rec.alts, list(rec.samples)[:5])
		print(dict(rec.samples['HG00096', 'HG00097']))
		if 'SVTYPE' in rec.info:
			print(i, rec.info['SVTYPE'])

		# if rec.alts[1]:
			# print(i, rec.pos, rec.format.keys(), rec.info.keys(),rec.ref, rec.qual, rec.alts)

		i += 1
		if i == 100:
			break


def create_row(res, gene, vcf_reader, samples):

	for rec in vcf_reader.fetch('19', *gene):
		# print(rec.CHROM, rec.var_type, rec.var_subtype, rec.start, rec.end, rec.QUAL, rec.POS, rec.REF, rec.ALT)

		row = [rec.POS, rec.REF, rec.ALT[0], rec.var_type, rec.var_subtype, rec.QUAL, 0]

		for sample in samples:
			# print(rec.genotype(sample).data.GT[0])
			row.append(rec.genotype(sample).data.GT[0])
			
		# print(len(row))

		res.append(row)



def vcf_with_vcf(asia=True):

	samples = asian_samples if asia else euro_samples
	vcf_reader = vcf.Reader(filename="./DataPop/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz",
	 compressed=True)
	cols = ['POS', 'REF', 'ALT', 'var_type', 'sub_type', 'QUAL', 'gene'] + samples


	res = []
	CHROM = None
	

	create_row(res, gene1, vcf_reader, samples)
	create_row(res, gene2, vcf_reader, samples)


	res = pd.DataFrame(res, columns=cols)

	res.to_pickle("./"+("asia" if asia else "euro")+"_vcf.pkl")

	return res




if __name__ == "__main__":
	asian_samples, euro_samples = load_data_from(), load_data_from(False)	
	gene1 = (10216899, 10225456)
	gene2 = (14063304, 14072254)
	# vcf_with_vcf()
	# vcf_with_vcf(False)

	df_asia = pd.read_pickle("./asia_vcf.pkl")
	df_euro = pd.read_pickle("./euro_vcf.pkl")

	process_data(df_euro)

	#add one column to each row:: prob 
	#then for each sample see if 1: prob if 0 1-prob





# http://dmnfarrell.github.io/bioinformatics/multi-sample-vcf-dataframe
