#!/usr/bin/python3
import pandas as pd
import sys

def main():
	try:
		num_simulations = int(sys.argv[1])
		is_traffic_light = str(sys.argv[2])
	except: 
	     print("Error: Need number of simulations or y/n for is_traffic_light")
	     return

	og_df = pd.DataFrame()

	for i in range(num_simulations+1):
		file_name = "simulation" + str(i) + ".csv"

		try:
			df = pd.read_csv(file_name, delimiter=',')
		except:
			print("couldn't open file CombineSimulations.py")
			continue

		og_df = og_df.append(df, ignore_index=True)

	if(is_traffic_light == "y"):
		output_path = str(num_simulations) + "_traffic_light_simulations.csv"	
	else:
		output_path = str(num_simulations) + "_simulations.csv"	

	og_df.to_csv(output_path, index=False)


main()
