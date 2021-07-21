import numpy as np
import collections


def load_sequences(filename, path="./"):
	return np.load(path+filename)
	

def kmer_count(k_spectra, sequence, k=5):

	for i in range(len(sequence) - k + 1):
		k_spectra[sequence[i:i+k]] += 1

	print(k_spectra)


if __name__ == "__main__":
	case = load_sequences(filename="case.npy")
	control = load_sequences(filename="control.npy")
	k = 5
	k_spectra = collections.defaultdict(int)

	print(case)
	print(control)
	
	
	kmer_count(sequence=case[4], k_spectra=k_spectra)
	