import numpy as np
import collections


def load_sequences(filename, path="./"):
	return np.load(path+filename)
	

def kmer_count(sequence, k=5):
	k_spectra = collections.defaultdict(int)
	for i in range(len(sequence) - k + 1):
		k_spectra[sequence[i:i+k]] += 1

	return(k_spectra)



if __name__ == "__main__":
	case = load_sequences(filename="case.npy")
	control = load_sequences(filename="control.npy")
	k = 5
	# k_spectra = collections.defaultdict(int)

	print(case)
	print(control)
	

	case_kspectra = list(map(kmer_count, case))
	control_kspectra = list(map(kmer_count, control))

	print(case_kspectra)

	# what should I think about... how can do it on one efficiently (the back and forth method)