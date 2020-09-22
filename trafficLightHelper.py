#!/usr/bin/python3
import pandas as pd 
import numpy as np
import sys

def main():
	try:
		simulation_path = str(sys.argv[1])
	except:
		print("Error: Fix arguments.. Simulation path")
		return

	df = pd.read_csv(simulation_path, delimiter=",")

	# Need to randomly generate x and y coordinates...
	df = df.drop('vehicle_x', axis=1)
	df = df.drop('vehicle_y', axis=1)

	new_df = pd.DataFrame(np.random.uniform(0.0, 5000.0, size=(df.shape[0], 2)), columns=['vehicle_x', 'vehicle_y'])

	df['vehicle_x'] = new_df['vehicle_x'].round(2)
	df['vehicle_y'] = new_df['vehicle_y'].round(2)

	# Stuff we do not want on any of them...
	df4 = df
	df4['Message'] = 4
	# df4 = df[df.brake_rate >= 1.0].reset_index(drop=True)
	# df4 = df4[df4.brake_rate < 2.0].reset_index(drop=True)
	# df4 = df4[df4.motionState_acceleration < 1450].reset_index(drop=True)
	# df4 = df4[df4.motionState_speed<= 1200].reset_index(drop=True)

	df5 = df
	df5['Message'] = 5
	# df5 = df5[df5.brake_rate >= 2.0].reset_index(drop=True)
	# df5 = df5[df5.brake_rate < 3.0].reset_index(drop=True)
	# df5 = df5[df5.motionState_acceleration < 1450].reset_index(drop=True)
	# df5 = df5[df5.motionState_speed<= 800].reset_index(drop=True)

	df6 = df
	df6['Message'] = 6
	# df6 = df6[df6.brake_rate >= 3.0].reset_index(drop=True)
	# df6 = df6[df6.motionState_acceleration < 1450].reset_index(drop=True)
	# df6 = df6[df6.motionState_speed < 400].reset_index(drop=True)


	# print(df4['vehicle_speed'].mean())
	# print(df5['vehicle_speed'].mean())
	# print(df6['vehicle_speed'].mean())

	df4.to_csv("IsoForest_Training_4.csv", index=False)
	df5.to_csv("IsoForest_Training_5.csv", index=False)
	df6.to_csv("IsoForest_Training_6.csv", index=False)

main()