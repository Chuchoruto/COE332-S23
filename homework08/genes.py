from flask import Flask, request, send_file
import requests
import redis
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, date
import io


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
        "POST" method: posts plot into redis db
        "GET" method: returns plot from redis db

    Returns:
        "DELETE" method: String confirming data deletion
        "POST" method: String confirming data posted
        "GET" method: returns plot from redis db in a file specified by udes
        
    '''


    if request.method == 'GET':
        if(len(rd_image.keys())== 0):
            return "No image in the database. use /image -X POST first.\n"
        else:
            plot_bytes = rd_image.get("Plot")

            # Load the bytes as an image
            buf = io.BytesIO(plot_bytes)
            buf.seek(0)
            # Return the image as a file to the user
            return send_file(buf, mimetype='image/png')
        
            
    # Make plot of Date vs ID number
    elif request.method == 'POST':
        if(len(rd.keys()) == 0):
            return "No data to create image from. please use /data -X POST first.\n"
        else:
            daysSince2000List = []
            HGNClist = []
            for item in rd.keys():
                
                value = rd.get(item).decode('utf-8')
                value = json.loads(value)
                date_str = value["date_approved_reserved"]
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                reference_date = date(2000, 1, 1)
                delta = parsed_date - reference_date
                days_since_2000 = delta.days
                daysSince2000List.append(days_since_2000)
                HGNClist.append(int(value["hgnc_id"][5:]))

            fig, ax = plt.subplots()
            ax.scatter(daysSince2000List, HGNClist,s=5,alpha=0.5)
            ax.set_title('ID Number vs Date Approved')
            ax.set_xlabel('Days since approval. Reference: January 1, 2000')
            ax.set_ylabel('HGNC ID number')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            rd_image.set("Plot", buf.getvalue())

            return 'Plot has been posted\n'

    elif request.method == 'DELETE':
        rd_image.flushdb()
        return f'Plot has ben deleted. There are {len(rd_image.keys())} plots in the db\n'

    
    
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
        if len(rd.keys()) == 0:
            return "The database is empty. Please post the data first\n"
        else:
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
    if len(rd.keys()) == 0:
        return "The database is empty. Please post the data first\n"

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