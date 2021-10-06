import numpy as np
import collections
import matplotlib.cm as clt
import matplotlib.pyplot as plt



#####GLOBAL SCOPE#####
k = 5
######################

def show_img(seq, i):
	global name 

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
	case = load_sequences(filename="case.npy")
	control = load_sequences(filename="control.npy")

	need_avg = True 
	need_img = True
	
	case_kspectra = list(map(kmer_count, case))
	control_kspectra = list(map(kmer_count, control))

	case_cgr = list(map(cgr_build, case_kspectra))
	control_cgr = list(map(cgr_build, control_kspectra))


	if need_img:
		# num_img = len(case_cgr)
		num_img = 5

		name = "case"
		done = list(map(save_img, case_cgr[:num_img], range(len(case_cgr[:num_img]))))

		name = "control"
		done = list(map(save_img, control_cgr[:num_img], range(len(control_cgr[:num_img]))))


		print(done)


	if need_avg:

		name = "case"
		avg_cgr(case_cgr)

		name = "control"
		avg_cgr(control_cgr)