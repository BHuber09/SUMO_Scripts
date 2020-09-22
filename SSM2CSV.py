#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys

def main():
	# column 0 is the vehicle id
	# column 1 is going to be the timestamp
	# column 2 is going to be the BR.
	df = pd.DataFrame()

	path = str(sys.argv[1])
	try: 
		f = open(path, "r")
		line = f.readline()

		while(line):
			if "values=" in line:
				line = line[:-4]

				if "timeSpan" in line:
					line = line[26:]
					data = line.split(" ")
					df['timestep_time'] = data
					#df['timestep_time'] = df['timestep_time'].astype(int)


				if "BRSpan" in line:
					line = line[24:]
					data = line.split(" ")
					df['brake_rate'] = data

			line = f.readline()


		df['vehicle_id'] = int(str(sys.argv[1][4:-4]))
		df['vehicle_id'].fillna(int(str(sys.argv[1][4:-4])))

		output = str(sys.argv[1][:-4]) + ".csv"
		df.to_csv(output, index=False)
	except:
		return


main()