import numpy as np
import collections
import matplotlib.cm as clt
import matplotlib.pyplot as plt
import glob
from Bio import SeqIO


from cgr import kmer_count, cgr_build, avg_cgr

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
			# print(repr(seq_record.seq))
			seq.append(str(seq_record.seq))

	seq = np.array(seq, dtype='str')

	print(seq.shape)
	print(len(seq[0]))

	return seq

def perform_cgr(seq, base):
	if need_rewrite:
		count_samples = list(map(kmer_count, seq))
		cgr_samples = np.array(list(map(cgr_build, count_samples)), dtype='int')

		np.save("cgrsamples"+name,cgr_samples)
	else:
		cgr_samples = np.load("cgrsamples"+name+".npy")
		print(cgr_samples.shape)
		print(cgr_samples)


	print(cgr_samples.shape)
	
	cgr_samples = cgr_samples - base

	mini = abs(min(np.amin(cgr_samples), 0)) + 1
	
	print(mini)

	cgr_samples = cgr_samples + mini 
	if need_avg:
		avg_chaos = np.mean(cgr_samples, axis=0)
		save_img(avg_chaos, "average")
		# return avg_chaos


	if need_img_ind:
		done = list(map(save_img, cgr_samples, range(num_img)))



def avg_whole(sample1, sample2):
	avg_chaos = np.mean([sample1, sample2], axis=0)
	show_img(avg_chaos, 'average')
	plt.savefig("avg_chaos.png")
	np.save("chaos.out", avg_chaos)	

if __name__ == "__main__":
	need_img_ind, need_avg, need_base, need_rewrite = True, True, False, False
	num_img = 40

	asia_seq = load_sequences()
	euro_seq = load_sequences(asia=False)

	# base_chaos = np.array(base_cgr(), dtype='int')
	# if need_base:
	# 	name = 'base'
	# 	show_img(base_chaos, 0)
	# 	plt.savefig("./base.png")


	avg_base = np.load('chaos.out.npy')
	# print(avg_base)


	name = 'AsianCGR'

	avg1 = perform_cgr(asia_seq, avg_base)

	name = 'EuroCGR'

	avg2 = perform_cgr(euro_seq, avg_base)

	# avg_whole(avg1, avg2)



	

