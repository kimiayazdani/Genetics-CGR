import numpy as np
import collections
import matplotlib.cm as clt
import pylab


def load_sequences(filename, path="./"):
	return np.load(path+filename)
	

def kmer_count(sequence):
	global k

	k_spectra = collections.defaultdict(int)

	for i in range(len(sequence) - k + 1):
		k_spectra[sequence[i:i+k]] += 1

	return(k_spectra)


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

	
	print(cgr_window)

	return cgr_window


if __name__ == "__main__":
	case = load_sequences(filename="case.npy")
	control = load_sequences(filename="control.npy")
	k = 3

	# print(case)
	# print(control)
	

	case_kspectra = list(map(kmer_count, case))
	control_kspectra = list(map(kmer_count, control))

	# print(case_kspectra)

	print(case_kspectra[0])



	cgr_window = cgr_build(case_kspectra[0])

	pylab.title("Chaos Game Representation for 0th Case")
	pylab.imshow(cgr_window, interpolation='nearest', cmap=clt.gray_r)

	pylab.show()


