import numpy as np

def sequence_generator():
	# a series of random sequences, half case half control. A number of case columns with probability of P to have A in control gp and C in case, o.w both A.

	alphabet = ['A', 'C', 'G', 'T']
	params = {'seq_num': 10, 'length': 1000, 'case_ok_cols': 60, 'prob_case': 1}


	sequences = np.random.choice(alphabet, (2, params['seq_num']//2, params['length']))
	case_ok_cols = np.random.choice(params['length'], params['case_ok_cols'], replace=False)
	print(case_ok_cols)

	sequences[:, :, [case_ok_cols]] = alphabet[0]



	case_cols = case_ok_cols[np.random.rand(len(case_ok_cols)) < params['prob_case']]
	sequences[0, :, [case_cols]] = alphabet[1]

	print(case_cols)

	print(sequences)

	#TODO: write in a file.
	np.save('seqs.out', sequences)


sequence_generator()