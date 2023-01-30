import json
import random


sites = {'sites':[]}

def main():
    for i in range(5):
        longitude = 82 + (2 * random.random())
        latitude = 16 + (2 * random.random())

        comp = random.choice(['stony', 'iron', 'stony-iron'])

        site_id = i + 1

        sites['sites'].append({'site_id': site_id, 
                               'latitude': latitude,
                               'longitude': longitude,
                               'composition': comp})



    
    with open('/home/lucal/COE332-S23/homework02/meteor_sites.json', 'w') as f:
        json.dump(sites, f, indent = 2)


if (__name__ == '__main__'):
    main()