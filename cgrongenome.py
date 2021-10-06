import numpy as np
import collections
import matplotlib.cm as clt
import matplotlib.pyplot as plt
import glob
from Bio import SeqIO

from cgr import kmer_count, cgr_build



def load_sequences(asia=True):
	path_asia, path_euro = glob.glob('./DataPop/AsianFastas/*'), glob.glob('./DataPop/EuroFastas/*')
	seq = list()
	file_path = path_asia if asia else path_euro

	for f in file_path:
		fast = SeqIO.parse(f, "fasta")
		for seq_record in fast:
			print(repr(seq_record.seq))
			seq.append(str(seq_record.seq))

	seq = np.array(seq, dtype='str')

	print(seq.shape)
	print(len(seq[0]))

	return seq

if __name__ == "__main__":
	asia_seq = load_sequences()
	euro_seq = load_sequences(asia=False)


	first_sample = kmer_count(asia_seq[0])
	first_cgr = cgr_build(first_sample)


