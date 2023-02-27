from flask import Flask
import xmltodict
import requests
import math

app = Flask(__name__)


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

# This method is called in the default curl command w/o more arguments
@app.route('/', methods = ['GET'])
def location() -> list:
    """
    This function returns all of the data in the set

    Args:
        NA
        
    Returns:
        A list of dictionaries that represent the data in the set of ISS Locations
    """
    data = get_data()
    return data

@app.route('/epochs', methods = ['GET'])
# Returns the list of all EPOCH names when called
def allEpochs()-> list:
    """
    This function returns all of the EPOCHs in the set

    Args:
        NA
        
    Returns:
        A list of Strings representing the EPOCHs in the set
    """
    data = get_data()
    epochs = []
    for e in data:
        epochs.append(e["EPOCH"])
    return epochs


# Returns the state vector for a sepcific EPOCH when called
@app.route('/epochs/<epoch>', methods = ['GET'])
def specEpoch(epoch: str) -> dict:
    """
    This takes a specific EPOCH string value and returns its state vector below

    Args:
        epoch: EPOCH string value for a specific time recorded for the ISS
        
    Returns:
        A dictionary of relevant data for the given epoch
    """
    data = get_data()
    for e in data:
        if (e["EPOCH"] == epoch):
            return e
    
    return "Error: Epoch not found\n"



@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def epochSpeed(epoch: str) -> dict:
    """
    This takes a specific EPOCH string value and returns the speed of the ISS at the given epoch

    Args:
        epoch: EPOCH string value for a specific time recorded for the ISS
        
    Returns:
        The speed of the ISS at the given EPOCH
    """
    
    data = get_data()
    for e in data:
        if (e["EPOCH"] == epoch):
            xV = float(e["X_DOT"]["#text"])
            yV = float(e["Y_DOT"]["#text"])
            zV = float(e["Z_DOT"]["#text"])
            speed = math.sqrt(xV*xV + yV*yV + zV*zV)
            return {"Speed": speed}
    
    return "Error: Epoch not found\n"








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
