#!/usr/bin/python3
import pandas as pd 
import numpy as np
import random
import sys
from sklearn.utils import shuffle

# add more data to car crashes??? where iso_df8.motionState_speed < 400

def main():
	try:
		file_name = str(sys.argv[1])
	except:
		print("Error. enter a filename")
		return

	df = pd.read_csv(file_name, delimiter=",")

	df0 = df[df.brake_rate == 0].reset_index(drop=True)
	df0 = df0[df0.vehicle_speed > 0].reset_index(drop=True)
	df0 = df0[df0.motionState_acceleration < 1450].reset_index(drop=True)
	df0['Message'] = 0

	df1 = df[df.brake_rate < 1].reset_index(drop=True)
	df1 = df1[df1.motionState_acceleration < 1450].reset_index(drop=True)
	df1['Message'] = 1

	df2 = df[df.brake_rate < 1].reset_index(drop=True)
	df2 = df2[df2.vehicle_speed > 0].reset_index(drop=True)
	df2 = df2[df2.motionState_acceleration < 1450].reset_index(drop=True)
	df2['Message'] = 2

	df3= df[df.brake_rate < 1].reset_index(drop=True)
	df3= df3[df3.vehicle_speed > 0].reset_index(drop=True)
	df3= df3[df3.motionState_acceleration >= 1450].reset_index(drop=True)
	df3['Message'] = 3

	df4 = df[df.brake_rate >= 1.0].reset_index(drop=True)
	df4 = df4[df4.brake_rate < 2.0].reset_index(drop=True)
	df4 = df4[df4.motionState_acceleration < 1450].reset_index(drop=True)
	df4 = df4[df4.motionState_speed<= 1200].reset_index(drop=True)
	df4['Message'] = 4

	df5 = df[df.brake_rate >= 2.0].reset_index(drop=True)
	df5 = df5[df5.brake_rate < 3.0].reset_index(drop=True)
	df5 = df5[df5.motionState_acceleration < 1450].reset_index(drop=True)
	df5 = df5[df5.motionState_speed<= 800].reset_index(drop=True)
	df5['Message'] = 5

	df6 = df[df.brake_rate >= 3.0].reset_index(drop=True)
	df6 = df6[df6.motionState_acceleration < 1450].reset_index(drop=True)
	df6 = df6[df6.motionState_speed < 400].reset_index(drop=True)
	df6['Message'] = 6

	new_df = df0
	new_df = new_df.append(df1, ignore_index=True)
	new_df = new_df.append(df2, ignore_index=True)
	new_df = new_df.append(df3, ignore_index=True)
	new_df = new_df.append(df4, ignore_index=True)
	new_df = new_df.append(df5, ignore_index=True)
	new_df = new_df.append(df6, ignore_index=True)

	#Since there is some overlap in the messages we need to remove duplicated messages.
	new_df = shuffle(new_df)
	new_df = new_df.drop_duplicates(subset=['timestep_time', 'vehicle_id'])


	new_df = new_df.sort_values(by='timestep_time')
	new_df.to_csv("FIXED_" + file_name, index=False)



main()

