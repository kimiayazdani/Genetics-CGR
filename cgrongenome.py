import numpy as np
import collections
import matplotlib.cm as clt
import matplotlib.pyplot as plt
import glob
from Bio import SeqIO


from cgr import kmer_count, cgr_build

def show_img(seq, i):
	global name 

	plt.title("Chaos Game Representation for " + name + ' ' + str(i))
	plt.imshow(seq, interpolation='nearest', cmap=clt.gray_r)


def save_img(seq, i):
	global name
	show_img(seq, i)

	plt.savefig("./DataPop/"+name+"/"+name+str(i)+".png")
	return i


def base_cgr():
	path_euro = glob.glob('./DataPop/EuroFastas/*00365*')
	for f in path_euro:
		print(f)
		fast = SeqIO.parse(f, "fasta")
		for seq_record in fast:
			fast = str(seq_record.seq)
			break

		return cgr_build(kmer_count(fast))

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

def perform_cgr(seq, base):
	count_samples = list(map(kmer_count, seq))
	cgr_samples = np.array(list(map(cgr_build, count_samples)), dtype='int')

	
	
	print(cgr_samples.shape)
	
	cgr_samples = cgr_samples - base

	mini = abs(np.amin(cgr_samples)) + 1

	print(mini)

	cgr_samples = cgr_samples + mini 

	done = list(map(save_img, cgr_samples, range(len(cgr_samples))))


if __name__ == "__main__":
	need_base = False

	asia_seq = load_sequences()
	euro_seq = load_sequences(asia=False)

	base_chaos = np.array(base_cgr(), dtype='int')
	if need_base:
		name = 'base'
		show_img(base_chaos, 0)
		plt.savefig("./base.png")


	name = 'AsianCGR'

	# perform_cgr(asia_seq, base_chaos)

	name = 'EuroCGR'

	perform_cgr(euro_seq, base_chaos)



	

