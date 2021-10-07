import os
import glob



def phase_two():
	files = glob.glob('./DataPop/AsianCGR/*.png')
	for f in files:
		os.remove(f)

	files = glob.glob('./DataPop/EuroCGR/*.png')
	for f in files:
		os.remove(f)

def phase_one():
	files = glob.glob('./case/*.png')
	for f in files:
		os.remove(f)

	files = glob.glob('./control/*.png')
	for f in files:
		os.remove(f)


if __name__ == "__main__":
	print("leave the poor files alone, hmm-k?")