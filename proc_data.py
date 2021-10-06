from Bio import SeqIO
import pandas as pd


def ancestry_separation():
	genomic_df = pd.read_csv('./DataPop/IGSR.csv', error_bad_lines=False)
	asian = genomic_df[genomic_df['Superpopulation code']=='EAS']
	europian = genomic_df[genomic_df['Superpopulation code']=='EUR']
	print(asian.shape)
	print(europian.shape)

	asian_samples = list(asian['Sample name'])[:25]
	europian_samples = list(europian['Sample name'])[:25]

	print(asian_samples)
	print(europian_samples)

	asian_file = open("./DataPop/asian.txt", 'w')
	euro_file = open("./DataPop/euro.txt", 'w')
	for i in range(25):
		asian_file.write(asian_samples[i] + '\n')
		euro_file.write(europian_samples[i] + '\n')

	asian_file.close()
	euro_file.close()


def test_read():
	fast = SeqIO.parse("./DataPop/AsianFastas/HG00404_out.fa", "fasta")
	for seq_record in fast:
		print(seq_record.id)
		print(repr(seq_record.seq))
		print(len(seq_record))
		fast = seq_record
		break

	print(fast.id)

	# print(fast.seq)
	print(fast.seq[0])

def readliness():
	file1 = open('./columns3', 'r')
	line1 = file1.readlines()
	i = 0
	for line in line1:
		print(len(line))
		for wrd in line.split():
			print(wrd)
		print(len(line))

if __name__ == "__main__":
	test_read()




#bash: while read p; do samtools faidx human_g1k_v37.fasta 19:10216899-10225456 | bcftools consensus -s $p ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz > ./AsianFastas/${p}_out.fa; echo $p; done < asian.txt