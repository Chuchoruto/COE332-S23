import json
import math

### mars radius in kilometers
mars_r = 3389.5 

with open('meteor_sites.json', 'r') as f:
    meteor_data = json.load(f)

def calculate_gcd(start_lat: float, start_long: float, end_lat: float, end_long: float) -> float:
    """
    The function input is the latitude and longitude of two points and it returns the distance between them

    Args:
        start_lat: Latitude of starting point
        start_long: longitude of starting point
        end_lat: latitude of ending point
        end_long: longitude of ending point 

    Returns:
        distance between 2 points which is calculated by the dsigma value * mars_r
    """
    lat1, lon1, lat2, lon2 = map( math.radians, [start_lat, start_long, end_lat, end_long] )
    dsigma = math.acos(math.sin(lat1)*math.sin(lat2) + (math.cos(lat1)*math.cos(lat2)*math.cos(abs(lon1-lon2))))
    return mars_r * dsigma



def calc_sample_time(composition):
    """
    The function calculates sample time based on the composition input

    Args:
        composition: type of composition ('stony', 'iron', 'stony-iron')

    Returns:
        sample_time: time required to sample in hours
    """
    if composition == 'stony-iron':
        sample_time = 3
    elif composition == 'iron':
        sample_time = 2
    elif composition == 'stony':
        sample_time = 1
    else:
        sample_time = 0
    
    return (sample_time)


def main():

    
    ### Keeps track of the current leg
    leg = 0

    ### Starting position of robot
    starting_latitude = 16.0
    starting_longitude = 82.0

    cumulative_time = 0

    for site in meteor_data['sites']:
        leg += 1

        ### Calculates sampling time of the next site
        next_composition = site['composition']
        sample_time = calc_sample_time(next_composition)

        ### Setting placeholders to calculate travel time.
        next_latitude = site['latitude']
        next_longitude = site['longitude']
        distance = calculate_gcd(starting_latitude, starting_longitude, next_latitude, next_longitude)
        travel_time = distance/10

        

        ### Prints each leg
        print('leg = %d, time to travel = %.2f hr, time to sample = %.2f hr' % (leg, travel_time, sample_time))

        
        ### Changes next iteration's starting point
        starting_latitude = next_latitude
        starting_longitude = next_longitude
        

        cumulative_time = cumulative_time + travel_time + sample_time
    
    print('===========================================')
    print('legs = %d, total time elapsed = %.2f hours' % (leg, cumulative_time))

    

if (__name__ == '__main__'):
    main()
