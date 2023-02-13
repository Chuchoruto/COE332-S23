
# Water Examination: Turbidity Calculation and Water Safety

This project calculates the turbidity of water and determines if it is safe or not.
If the water is not safe, it will also calculate how long until it is safe according to turbidity decay.

### Data Used

The data used is accessed from the link https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json
It is loaded into the script via API request from the Python requests library as follows

```
import requests
import json

response = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
turb_data = response.json()['turbidity_data']
```


### Script Description
test.py
- This script unit tests the functions called in the next script to ensure they are working properly

water_examination.py
- This script examines the data pulled in from the request and outputs the water's turbidity, if it's above or below the safety threshold, and time to return below the threshold

### INSTRUCTIONS TO RUN

First run the unit tests to ensure that the functions are working properly as shown below
```
pytest -q test.py
```

This should yield output similar to
```
[100%]
2 passed in 0.07s
```

Next, run the water examination script in the terminal as shown below
```
python3 water_examination.py
```

this should yield an output similar to:
```
Average turbidity based on most recent five measurements = 1.1506 NTU
Warning: Turbidity is above threshold for safe use
Minimum time required to return below a safe threshold = 6.95 hours
```

These results show that the water is not currently safe for use because the turbidity is over 1 NTU. It also shows that the water will be safe again in 6.95 hours.

In the case that the water is already safe, the output will look more like this:
```
Average turbidity based on most recent five measurements = 0.506 NTU
Info: Turbidity is below threshold for safe use
Minimum time required to return below a safe threshold = 0.00 hours
```