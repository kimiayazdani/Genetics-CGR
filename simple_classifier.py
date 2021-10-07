import numpy as np
from cgrongenome import adjust



def classifier(seq):
	asian = np.sum(np.abs(seq-avg_asia))
	euro = np.sum(np.abs(seq-avg_euro))
	# print(asian)
	# print(euro)

	return "asian" if asian < euro else "euro"





if __name__ == "__main__":
	name_asia, name_euro = 'AsianCGR', 'EuroCGR'

	avg_asia = np.load('avgfinal' + name_asia + '.npy')
	avg_euro = np.load('avgfinal' + name_euro +'.npy')

	# print(avg_euro)
	# print(avg_asia)
	# print(avg_asia.shape)
	# print(avg_euro.shape)


	avg_base = np.load('chaos.out.npy')
	# print(avg_base.shape)


	asia_samples = np.load('cgrsamples'+name_asia+'.npy')
	euro_samples = np.load('cgrsamples'+name_euro+'.npy')
	# print(adjust)

	# print(asia_samples.shape)
	# print(euro_samples.shape)
	for sam in euro_samples:
		print(classifier(sam))

	print("----")
	for sam in asia_samples:
		print(classifier(sam))
	# classifier(asia_samples[0])
	# classifier(euro_samples[5])






#what to fix?: that the samples are built with two different genomes in a non-consistent way :( I should once perform e.th