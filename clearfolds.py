import os
import glob


def delete_files(path):
	files = glob.glob(path)
	for f in files:
		os.remove(f)


def phase_two():
	delete_files('./DataPop/AsianCGR/*.png')
	delete_files('./DataPop/EuroCGR/*.png')

def phase_one():
	delete_files('./case/*.png')
	delete_files('./control/*.png')


if __name__ == "__main__":
	print("leave the poor files alone, hmm-k?")
