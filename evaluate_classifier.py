from cgrongenome import load_sequences
import collections
import json


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
			try:
				probs[i][seq[j][i]] += 1
			except:
				print(i, j,"why :(")


	with open(("asia" if asia else "euro")+"_probs.txt", "w") as fp:
		json.dump(probs, fp)





if __name__ == "__main__":
	asia_seq = load_sequences()
	euro_seq = load_sequences(False)
	genome_len = len(asia_seq[0])

	# print(len(asia_seq), len(euro_seq))

	# check_duality(asia_seq)
	# check_duality(euro_seq, asia=False)

	# print(load_prop()[:1000])

	# try catch error on euro - 17508 5 why :( 17508 424 why