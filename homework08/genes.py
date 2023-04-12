from flask import Flask, request
import requests
import redis
import json
import os
import matplotlib.pyplot as plt


app = Flask(__name__)

def get_redis_client():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=0)

def get_redis_image_db():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=1)

rd = get_redis_client()

rd_image = get_redis_image_db()





@app.route('/image', methods = ['POST', 'GET', 'DELETE'])
def ret_image():
    '''
    Manipulates image data with GET, POST, and DELETE methods
    
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
        someurl = "imgur url"
        return someurl
    
    elif request.method == 'POST':
        
        return 'Data has been posted\n'

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'Data had ben deleted. There are {len(rd.keys())} keys in the db\n'

    
    
    else:
        return 'the method you tried does not work\n'






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
            value = rd.get(item).decode('utf-8')
            if value is not None and value.strip():
                output_list.append(json.loads(value))
        return output_list
    
    elif request.method == 'POST':
        response = requests.get(url= 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            rd.set(key, json.dumps(item))
        return 'Data has been posted\n'

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'Data had ben deleted. There are {len(rd.keys())} keys in the db\n'

    
    
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

    for key in rd.keys():
        key = key.decode('utf-8')
        hgnc_list.append(key)
    return hgnc_list


@app.route('/genes/<hgnc_id>', methods = ['GET'])
def get_hgnc(hgnc_id) -> dict:
    '''
    Return all data associated with <hgnc_id>

    Args:
        hgnc_id:    The unique hgnc ID of the gene in the data set
    
    Returns:
        all data associated with the given <hgnc_id>
    '''
    if len(rd.keys()) == 0:
        return "The database is empty. Please post the data first\n"

    for key in rd.keys():
        if key.decode('utf-8') == hgnc_id:
            return json.loads(rd.get(key))

    return "Given hgnc_id did not match any in the database\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')