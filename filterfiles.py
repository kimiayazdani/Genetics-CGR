import os
import glob

def remove_empty(asia=True):
	asian_path, euro_path = glob.glob('./DataPop/AsianFastas/*'), glob.glob('./DataPop/EuroFastas/*')
	right_path = asian_path if asia else euro_path
	for f in right_path:
		# print(os.path.getsize(f), f)
		if os.path.getsize(f) < 1:
			print(os.path.getsize(f), f)
			# os.remove(f)



def counterfiles():
	#just to apply later
	asian_path, euro_path = glob.glob('./DataPop/AsianFastas/*'), glob.glob('./DataPop/EuroFastas/*')
	for f in asian_path:
		print(f)
		print(f[:-3]+'_two.fa')	

		fast = SeqIO.parse(f, "fasta")
		for seq_record in fast:
			print(repr(seq_record.seq))
			seq.append(str(seq_record.seq))

		f2 = f[:-3]+'_two.fa'
		fast = SeqIO.parse(f2, "fasta")
		for seq_record in fast:
			print(repr(seq_record.seq))
			seq[-1].append(str(seq_record.seq))

		break


if __name__ == "__main__":
	# remove_empty()
	# remove_empty(asia=False)
	counterfiles()