import os
import glob

def remove_empty():
	asian_path, euro_path = glob.glob('./DataPop/AsianFastas/*'), glob.glob('./DataPop/EuroFastas/*')
	for f in asian_path:
		# print(os.path.getsize(f), f)
		if os.path.getsize(f) < 1:
			print(os.path.getsize(f), f)
			# os.remove(f)

if __name__ == "__main__":
	remove_empty()