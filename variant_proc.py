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


def process_data(asia=True):
	df = df_asia if asia else df_euro
	# print(df.shape)
	only_snp = df[df.var_type=='snp']
	sample_GT = only_snp[df.columns[7:]]
	# sample_GT['zeroes'] = (sample_GT==0).astype(int).sum(axis=1)
	# sample_GT['ones'] = (sample_GT==1).astype(int).sum(axis=1)
	sample_GT['SUM'] = sample_GT.sum(axis=1)
	# print(len(sample_GT.columns))

	sample_GT[('A' if asia else 'E')+'PROB'] = sample_GT['SUM']/len(sample_GT.columns)
	sample_GT[('A' if asia else 'E')+'1-PROB'] = 1 - sample_GT[('A' if asia else 'E')+'PROB']

	# print(sample_GT[['SUM',('A' if asia else 'E')+'PROB',('A' if asia else 'E')+'1-PROB']])

	return sample_GT

def add_probs(asia=True):
	df = asia_sampleGT if asia else euro_sampleGT
	other_df = euro_sampleGT if asia else asia_sampleGT

	query = ('E' if asia else 'A')
	df[query+'PROB'] = other_df[query+'PROB']
	df[query+'1-PROB'] = other_df[query+'1-PROB']

	

def vcf_with_pysam():
	bcf_in = VariantFile("./DataPop/ALL.chr19.phase3_integrated.20130502.genotypes.bcf")
	print(list(bcf_in.header.info))
	for rec in bcf_in.fetch():
		print(i, rec.pos, rec.format.keys(), rec.info.keys(),rec.ref, rec.qual, rec.alts, list(rec.samples)[:5])
		print(dict(rec.samples['HG00096', 'HG00097']))
		if 'SVTYPE' in rec.info:
			print(i, rec.info['SVTYPE'])


def create_row(res, gene, vcf_reader, samples):

	for rec in vcf_reader.fetch('19', *gene):
		# print(rec.CHROM, rec.var_type, rec.var_subtype, rec.start, rec.end, rec.QUAL, rec.POS, rec.REF, rec.ALT)

		row = [rec.POS, rec.REF, rec.ALT[0], rec.var_type, rec.var_subtype, rec.QUAL, 0]

		for sample in samples:
			# print(rec.genotype(sample).data.GT[0])
			# row.append(rec.genotype(sample).data.GT[0])

			n = int(rec.genotype(sample).data.GT[0])
			if n != 0 and n != 1:
				n = 1

			row.append(n)
			
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


def calc_anc_for_samples(df):
	print(asia_sampleGT.shape)

	make_prob = lambda samp: samp*df[name+'PROB']+(1-samp)*df[name+'1-PROB']

	for name in ['A','E']:
		df.loc['TOTAL'+name, :] = df[df.columns[:-3]].apply(make_prob).sum(axis=0)

	# print(df)

def calc_winner(asia=True):
	df = asia_sampleGT if asia else euro_sampleGT



	df.loc['CORRECT',:] = (df.loc['TOTAL'+['E','A'][asia],:]>df.loc['TOTAL'+['A','E'][asia],:]).astype(int)
	return df.loc['CORRECT',:].sum(axis=0)
	# print(df)


if __name__ == "__main__":
	asian_samples, euro_samples = load_data_from(), load_data_from(False)	
	num_asia, num_euro = len(asian_samples), len(euro_samples)
	gene1 = (10216899, 10225456)
	gene2 = (14063304, 14072254)

	# vcf_with_vcf()
	# vcf_with_vcf(False)

	df_asia = pd.read_pickle("./asia_vcf.pkl")
	df_euro = pd.read_pickle("./euro_vcf.pkl")


	asia_sampleGT = process_data()
	euro_sampleGT = process_data(False)

	# print(asia_sampleGT)
	# print(euro_sampleGT)

	# asia_sampleGT['EPROB'] = euro_sampleGT['EPROB']
	add_probs()
	add_probs(False)

	calc_anc_for_samples(asia_sampleGT)
	calc_anc_for_samples(euro_sampleGT)

	# print(asia_sampleGT)
	# print(euro_sampleGT)

	correct = calc_winner(False) + calc_winner()
	print(correct)
	print(correct/(num_asia+num_euro))

	# add one row for % of euro , one for % of asia. then for asia if asia bigger: 1 for euro reverse



	# ok the thing is: add one row for each sample with 1/0 1:right-0:wrong
