from cgrongenome import load_sequences
import collections
import json
import vcf


def load_prop(asia=True):
	with open(('asia' if asia else 'euro')+"_probs.txt", "r") as fp:
		return json.load(fp)

def check_duality(seq, asia=True):
	global genome_len

	probs = list()

	for i in range(genome_len):
		probs.append(collections.defaultdict(int))

	genome_len = genome_len

	for i in range(genome_len):
		for j in range(len(seq)):
			if len(seq[j]) != genome_len:
				print(j, "jumping")
				continue
			try:
				probs[i][seq[j][i]] += 1
			except:
				print(i, j,"This is a sign of deletion!")


	with open(("asia" if asia else "euro")+"_probs.txt", "w") as fp:
		json.dump(probs, fp)







if __name__ == "__main__":
	asia_seq = load_sequences()
	euro_seq = load_sequences(False)
	genome_len = len(asia_seq[0])

	# print(len(asia_seq), len(euro_seq))

	# list_t = list()
	# for i,seq in enumerate(euro_seq):
	# 	if len(seq) != genome_len:
	# 		print(i, len(seq))
	# 		list_t.append(i)

	# print(len(list_t))


	# check_duality(asia_seq)
	# check_duality(euro_seq, asia=False)

	# asia_nums = load_prop()
	# euro_nums = load_prop(asia=False)


	# for i in range(1700):
		# if asia_nums[i].keys() != euro_nums[i].keys():
			# print(asia_nums[i].keys(), euro_nums[i].keys())



	# print(load_prop()[:1000])


	

