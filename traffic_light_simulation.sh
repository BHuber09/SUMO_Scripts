#!/bin/bash
clear

if [ $# -eq 0 ]
  then
    echo "Error: Enter the number of simulations to run.."
    exit 1
fi



# i = number of simulations to run... 
for i in $(seq 0 1 $1); do
	echo "Run $i"
	cd ~/school/thesis/sumo_stuff/

	# echo " "
	echo "Generating new trips."
	python3 ~/sumo-0.32.0/tools/randomTrips.py -n map.net.xml -r map.rou.xml -e 50 --length

	echo " "
	echo "Running sumo."
	#sumo -c map.sumocfg --fcd-output FCD-Trace.xml  --amitran-output Trajectories.xml --netstate-dump RAW-position.xml --lanechange-output LaneChange-output.xml  
	sumo -c map.sumocfg --fcd-output FCD-Trace.xml  --lanechange-output LaneChange.xml --device.ssm.probability 1 --amitran-output Trajectories.xml

	mv FCD-Trace.xml ../simulations 
	mv LaneChange.xml ../simulations
	mv ssm_* ../simulations/
	mv Trajectories.xml ../simulations
	# mv RAW-position.xml ../simulations

	cd ../simulations

	echo " "
	echo "--Converting xml to csv--"
	python3 ~/sumo-0.32.0/tools/xml/xml2csv.py FCD-Trace.xml
	python3 ~/sumo-0.32.0/tools/xml/xml2csv.py LaneChange.xml
	python3 ~/sumo-0.32.0/tools/xml/xml2csv.py Trajectories.xml
	# python3 ~/sumo-0.32.0/tools/xml/xml2csv.py RAW-position.xml

	rm FCD-Trace.xml
	rm Trajectories.xml
	rm LaneChange.xml

	echo " "
	echo "--Converting SSM to csv--"
	count=0
	for filename in ssm_*.xml; do
		let "count += 1"
		python3 SSM2CSV.py "$filename"

		# if exit 1; then
		# 	echo "Error.. Exiting."
		# 	exit 1 
		# fi

		# Delete the file we just changed to csv.
		rm "$filename"
	done

	echo " "
	echo "Standardizing sumo outputs"
	python3 standardizeOutputs.py "$i" "$count"

	# delete the files we don't need anymore.
	rm FCD-Trace.csv
	rm LaneChange.csv
	rm ssm_*.csv
	rm Trajectories.csv
done

if [ $1 -eq 0 ]; then
	exit 1
fi
python3 combineSimulations.py "$1" "y"
rm simulation*


# now we have our simulation... we need to take all of these simulations and combine them.. then do some analysis..
python3 trafficLightHelper.py "$1_traffic_light_simulations.csv"

