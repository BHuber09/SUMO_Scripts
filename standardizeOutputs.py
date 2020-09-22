#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys

# THIS FILE IS SUPER IMPORTANT.
# It takes alle the files that sumo outputs, gets the fields we want from them and combines them into 1 file
# Then it also removes all the columns we don't want
# It also a

# ToDo: Add dtype to the pandas read csv function. it'll be faster.

def main():
    try:
        num_simulations = int(sys.argv[1])
        num_ssm_files = int(sys.argv[2])
    except: 
        print("Error: Fix arguments 1 = num_simulations, 2 = num_ssm_files")
        return 


    # Get the existing files that have been digested..
    fcd_df = readFCD("FCD-Trace.csv")
    #lane_df = readLane("LaneChange.csv")
    ssm_df = readSSMs(num_ssm_files)
    traj_df = readTraj("Trajectories.csv")

    fcd_cols = list(fcd_df.columns)
    #lane_cols = list(lane_df.columns)
    ssm_cols = list(ssm_df.columns)
    traj_cols = list(traj_df.columns)


    # This does an outer join, but has tons of blanks in it which are useless..
    # join the original df's into our new one..
    df = pd.merge(fcd_df, traj_df, on=[fcd_cols[0], fcd_cols[1]], how='outer')
    # join ssm to the combined one..
    df = pd.merge(df, ssm_df, on=[fcd_cols[0], fcd_cols[1]], how='outer')
    # join lane to the combined one..
    #df = pd.merge(df, lane_df, on=[fcd_cols[0], fcd_cols[1]], how='outer')

    #  # join the original df's into our new one..
    # df = pd.merge(fcd_df, traj_df, on=[fcd_cols[0], fcd_cols[1]])
    # # join ssm to the combined one..
    # df = pd.merge(df, ssm_df, on=[fcd_cols[0], fcd_cols[1]])
    # # join lane to the combined one..
    # df = pd.merge(df, lane_df, on=[fcd_cols[0], fcd_cols[1]])

    # Randomly generating non-important anomalies..
    # anomalies = []
    # for i in range(df.shape[0]):
    #     anomalies.append(np.random.choice([0,1,2,3,4,5]))
    # df['message'] = anomalies


    # DELETE ROWS with null values....
    df = df.dropna(how='any', axis=0)

    # write the file to the output..
    file_name = "simulation" + str(num_simulations) + ".csv"
    df.to_csv(file_name, index=False)

    # print("FCD")
    # print(fcd_df)
    # print("TRAJ")
    # print(traj_df)
    # print("SSM")
    # print(ssm_df)
    # print("LANE")
    # print(lane_df)




def readFCD(path):
    df = pd.read_csv(path, delimiter=';')

    # timestep_time, vehicle_angle, vehicle_id, vehicle_lane, vehicle_pos, vehicle_slope, vehicle_speed, vehicle_type, vehicle_x, vehicle_y
    fcd_cols = list(df.columns)

    # remove: vehicle_angle, vehicle_lane, vehicle_slope, vehicle_type, 
    df = df.drop(fcd_cols[1], axis=1)
    df = df.drop(fcd_cols[3], axis=1)
    df = df.drop(fcd_cols[5], axis=1)
    df = df.drop(fcd_cols[7], axis=1)

    return df


def readLane(path):
    df = pd.read_csv(path, delimiter=';')

    lane_cols = list(df.columns)

    df = df.drop(lane_cols[0], axis=1)
    # 1 == followergap
    df = df.drop(lane_cols[2], axis=1)
    df = df.drop(lane_cols[3], axis=1)
    df = df.drop(lane_cols[4], axis=1)
    # 5 == id
    df = df.drop(lane_cols[6], axis=1)
    df = df.drop(lane_cols[7], axis=1)
    df = df.drop(lane_cols[8], axis=1)
    df = df.drop(lane_cols[9], axis=1)
    df = df.drop(lane_cols[10], axis=1)
    df = df.drop(lane_cols[11], axis=1)
    df = df.drop(lane_cols[12], axis=1)
    df = df.drop(lane_cols[13], axis=1)
    df = df.drop(lane_cols[14], axis=1)
    # 16 == timestep
    df = df.drop(lane_cols[16], axis=1)
    df = df.drop(lane_cols[17], axis=1)

    # renaming them because that is just gross...
    df = df.rename(columns={lane_cols[1]: "follower_gap", lane_cols[5]: "vehicle_id", lane_cols[15]: "timestep_time"})

    df["timestep_time"] = df["timestep_time"].div(10)
    df["timestep_time"] = df["timestep_time"].astype(int)

    df = df.reset_index(drop=True)

    return df



def readSSMs(num_ssms):
    df = pd.DataFrame()
    for i in range(num_ssms):
        file_name = "ssm_" + str(i) + ".csv"
        try:
            new_df = pd.read_csv(file_name, delimiter=",")
        except: 
            continue

        df = df.append(new_df)

    return df


# col12 = timestep... col13 is vehicle_id at that timestamp.
def readTraj(path):
    df = pd.read_csv(path, delimiter=';')

    # trajectories_timeStepSize, actorConfig_emissionClass, actorConfig_fuel, actorConfig_id, actorConfig_ref, actorConfig_vehicleClass, vehicle_actorConfig, vehicle_id, vehicle_ref, vehicle_startTime, motionState_acceleration, motionState_speed, motionState_time, motionState_vehicle
    traj_cols = list(df.columns)

    # Remove: stuff we don't need.
    for i in range(10):
        df = df.drop(traj_cols[i], axis=1)

    # now drop empty or 0's in acceleration, speed, and time. 
    df = df.dropna(subset=[traj_cols[10], traj_cols[11], traj_cols[12], traj_cols[13]])

    # drop duplicated rows...
    df.drop_duplicates(subset=[traj_cols[10], traj_cols[11], traj_cols[12], traj_cols[13]]).reset_index(drop=True)

    # convert the timestamp to 0-x, instead of the 1000 incremements
    df[traj_cols[12]] = df[traj_cols[12]].div(1000)
    df = df.astype(int)

    df = df.reset_index(drop=True)

    # rename the column to what we want...
    df = df.rename(columns={traj_cols[12]: 'timestep_time', traj_cols[13]: 'vehicle_id'})

    return df





main()