from flask import Flask, request
import requests
import redis
import json


app = Flask(__name__)

def get_redis_client():
    return redis.Redis(host='0.0.0.0', port=6379, db=0)
rd = get_redis_client()




@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def ret_data():
    '''
    Manipulates data with GET, POST, and DELETE methods
    
    Args: None

    Methods:
        "DELETE" method: deletes all data in redis db
        "POST" method: posts data into redis db
        "GET" method: returns data from redis db

    Returns:
        "DELETE" method: String confirming data deletion
        "POST" method: String confirming data posted
        "GET" method: returns data from redis db in the form of a list of dictionaries
        
    '''

    if request.method == 'GET':
        output_list = []
        for item in rd.keys():
            output_list.append(json.loads(rd.get(item)))
        return output_list
    
    elif request.method == 'POST':
        response = requests.get(url= 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            rd.set(key, json.dumps(item))
        return 'data posted\n'

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted there are {len(rd.keys())} keys in the db\n'
    
    else:
        return 'the method you tried does not work\n'


@app.route('/genes', methods = ['GET'])
def get_hgnc_list() -> list:
    '''
    Creates and returns a list of all hgnc_ids

    Args: NONE

    Returns:
        hgnc_list: List of all the hgnc IDs
    '''
    hgnc_list = []

    for item in rd.keys():
        hgnc = json.loads(rd.get(item))
        key = hgnc["hgnc_id"]
        hgnc_list.append(key)
    return hgnc_list


    





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')