#!/usr/bin/python3
import pandas as pd 
import sys

def main():	
	try:
		file_name = str(sys.argv[1])
	except: 
	     print("Error: Need file name of the simulations")
	     return

	df = pd.read_csv(file_name, delimiter=',')


	df_6 = df[df.brake_rate < 1.0].reset_index(drop=True)

	df_7 = df[df.brake_rate > 1.0].reset_index(drop=True)
	df_7 = df_7[df_7.brake_rate < 2.0].reset_index(drop=True)

	df_8 = df[df.brake_rate > 2.0].reset_index(drop=True)

	df_6.to_csv("IsoForest_Training_6.csv", index=False)
	df_7.to_csv("IsoForest_Training_7.csv", index=False)
	df_8.to_csv("IsoForest_Training_8.csv", index=False)


main()