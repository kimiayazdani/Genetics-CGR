import os
import glob

if __name__ == "__main__":
	files = glob.glob('./case/*.png')
	for f in files:
		os.remove(f)

	files = glob.glob('./control/*.png')
	for f in files:
		os.remove(f)