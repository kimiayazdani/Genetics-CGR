import numpy as np 

def convert_to_str():
	path, filename = './', 'seqs.out.npy'
	sequences = np.load(path+filename)

	to_str = lambda list: ''.join(list)

	case_gp = np.array(list(map(to_str, sequences[0, :, :])))
	control_gp = np.array(list(map(to_str, sequences[1, :, :])))
	
	print(control_gp)
	print(case_gp)
	print(sequences)

	np.save("case", case_gp)
	np.save("control", control_gp)



convert_to_str()