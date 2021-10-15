from pysam import VariantFile
import pysam
import numpy as np
import glob
import pandas as pd
import vcf
import gzip

def load_data_from(asia=True):
	samples = list()
	asian_path, euro_path = glob.glob('./DataPop/AsianFastas/*t.fa'), glob.glob('./DataPop/EuroFastas/*t.fa')
	right_path = asian_path if asia else euro_path
	for f in right_path:
		samples.append(f[-14:-7])

	return samples

	

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

def vcf_with_vcf():
	vcf_reader = vcf.Reader(filename="./DataPop/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz",
	 compressed=True)
	cols = ['sample','REF','ALT','mut','DP','ADF','ADR','AD','chrom','var_type','sub_type','start','end','QUAL']
	# print(vcf_reader.infos)

	#'19', 10216899, 10225456
	#vcf.filters.SnpOnly(args)

	CHROM = None
	for rec in vcf_reader.fetch('19', *gene1):
		print(rec.CHROM, rec.var_type, rec.var_subtype, rec.start, rec.end, rec.QUAL, rec.POS)
		for sample in asian_samples:
			print(rec.genotype(sample).data.GT[0])
			break

		break

	# print(vcf_reader.fetch(CHROM))
	




if __name__ == "__main__":
	asian_samples, euro_samples = load_data_from(), load_data_from(False)	
	gene1 = (10216899, 10225456)
	gene2 = (14063304, 14072254)
	# vcf_with_pysam()
	vcf_with_vcf()


#alan farz konim filter kardam ye seri satr o sootoon ro, hala az in bein ma mikhaim daghighan chi kar konim
#age mitoonestam in ro mesle pandas baz konam benazaram kheili khoob bood, ya hata chizaii ke baiad ro bardaram
#tabdilesh konam be df e panda save konam
#chi mikham bardaram? alts, GT[0], sample ha ro joda chiz mikonam yani ye doc bara euro yeki bara asia,
#baad oonja ba amaliat e filter va baad jam o tghsim bar tedad handle esh mikonam

# sootoona : sample ha, ref ha, alt ha, var_type, subtype, QUAL - radif: POS


# http://dmnfarrell.github.io/bioinformatics/multi-sample-vcf-dataframe
