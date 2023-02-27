from flask import Flask, request
import xmltodict
import requests
import math

app = Flask(__name__)

data = {}


def get_data():
    """
    This function returns all of the data in the set

    Args:
        NA
        
    Returns:
        A list of dictionaries that represent the data in the set of ISS Locations
    """

    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data['ndm']['oem']['body']['segment']['data']['stateVector']

data = get_data()

# This method is called in the default curl command w/o more arguments
@app.route('/', methods = ['GET'])
def location():
    """
    This function returns all of the data in the set

    Args:
        NA
        
    Returns:
        A list of dictionaries that represent the data in the set of ISS Locations
    """
    global data
    
    return data

@app.route('/epochs', methods = ['GET'])
# Returns the list of all EPOCH names when called
def allEpochs():
    """
    This function returns all of the EPOCHs in the set

    Args:
        NA
        
    Returns:
        A list of Strings representing the EPOCHs in the set
    """
    global data
    
    try:
        limit = int(request.args.get('limit', len(data)))
    except ValueError:
        return "Bad input\n",400

    try:
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return "Bad input\n",400

    
    epochs = []
    totalResults = 0
    index = 0
    for e in data:
        if(limit == totalResults):
            break
        if(index >= offset):
            epochs.append(e["EPOCH"])
            totalResults+= 1
            
        index += 1
    return epochs


# Returns the state vector for a sepcific EPOCH when called
@app.route('/epochs/<epoch>', methods = ['GET'])
def specEpoch(epoch: str):
    """
    This takes a specific EPOCH string value and returns its state vector below

    Args:
        (String) sepoch: EPOCH string value for a specific time recorded for the ISS
        
    Returns:
        A dictionary of relevant data for the given epoch
    """
    global data

    for e in data:
        if (e["EPOCH"] == epoch):
            return e
    
    return "Error: Epoch not found\n"



@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def epochSpeed(epoch: str):
    """
    This takes a specific EPOCH string value and returns the speed of the ISS at the given epoch

    Args:
        (String) epoch: EPOCH string value for a specific time recorded for the ISS
        
    Returns:
        The speed of the ISS at the given EPOCH
    """
    
    global data

    for e in data:
        if (e["EPOCH"] == epoch):
            xV = float(e["X_DOT"]["#text"])
            yV = float(e["Y_DOT"]["#text"])
            zV = float(e["Z_DOT"]["#text"])
            speed = math.sqrt(xV*xV + yV*yV + zV*zV)
            return {"Speed": speed}
    
    return "Error: Epoch not found\n"


@app.route('/delete-data', methods = ['DELETE'])
def deleteData():
    global data
    del data
    return "Data deleted\n"



@app.route('/post-data', methods = ['POST'])
def postData():
    global data
    data = get_data()
    
    return "Data Posted Successfully\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
