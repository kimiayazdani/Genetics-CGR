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

if __name__ == "__main__":
	remove_empty()
	remove_empty(asia=False)