====================================================
Mars Rover: Site Distance and Time Calculation Tool
====================================================

This project simulates travel time of a Mars Rover within a certain surface area of Mars.
It generates five meteor sites, calculates the time necessary to travel between them and investigate them, and thenprints the output of each leg and the cumulative time to the terminal.

====================================================
Script Description
----------------------------------------------------
site_generation.py
Generates five different meteor sites and stores them in a dictionary in a json file

----------------------------------------------------
time_calculation.py

Calculates the travel and sample time on each leg of the rover's journey.
Also calculates the cumulative time of the trip and the total legs associated with the journey.


====================================================
INSTRUCTIONS TO RUN

Run the site_generation.py script and then the time_calculation.py script in the same directory.
This will print a list of travel times and sample times for each of n legs as well as the total investigation time.
Each leg shows travel time from the previous leg or starting position to the next meteor site.
====================================================
