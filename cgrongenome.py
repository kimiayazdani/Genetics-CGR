import numpy as np
import collections
import matplotlib.cm as clt
import matplotlib.pyplot as plt
import glob
from Bio import SeqIO

def show_img(seq, i):
	plt.title("Chaos Game Representation for " + name + ' ' + str(i))
	plt.imshow(seq, interpolation='nearest', cmap=clt.gray_r)

def save_img(seq, i):
	global name
	show_img(seq, i)

	plt.savefig("./"+name+"/"+name+str(i)+".png")
	return i


def load_sequences(filename, path="./"):
	return np.load(path+filename)
	

def kmer_count(sequence):
	global k

	k_spectra = collections.defaultdict(int)

	for i in range(len(sequence) - k + 1):
		k_spectra[sequence[i:i+k]] += 1

	return(k_spectra)


def avg_cgr(sequence):
	avg_chaos = np.mean(sequence, axis=0)

	save_img(avg_chaos, "avg")

def cgr_build(kmers):
	global k


	# Positions in CGR window:#
	#		A 		C 		  #
	#						  #
	#						  #
	#		T 		G 		  #
	###########################

	windsize = 2 ** k
	max_x, pos_x = windsize, 1
	max_y, pos_y = max_x, 1

	to_add_x = {'A': '0', 'T': 'max_x/2', 'C': '0', 'G': 'max_x/2'}
	to_add_y = {'A': '0', 'T': '0', 'C': 'max_y/2', 'G': 'max_y/2'}

	cgr_window = [[0 for i in range(max_x)] for j in range(max_y)]

	for key, val in kmers.items():
		for char in key:
			pos_x += eval(to_add_x[char])
			pos_y += eval(to_add_y[char])
			max_x /= 2
			max_y /= 2

		cgr_window[int(pos_x-1)][int(pos_y-1)] = val
		max_x, max_y = windsize, windsize
		pos_x, pos_y = 1, 1


	return cgr_window

if __name__ == "__main__":
	asian_files = glob.glob('./DataPop/AsianFastas/*')
	asian_seqs = list()
	for f in asian_files:
		fast = SeqIO.parse(f, "fasta")
		for seq_record in fast:
			print(repr(seq_record.seq))
			asian_seqs.append(str(seq_record.seq))

	asian_seqs = np.array(asian_seqs, dtype='str')
	print(len(asian_seqs))

	print(asian_seqs.shape)
	print(asian_seqs[0])



		