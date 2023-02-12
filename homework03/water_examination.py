import json
import requests
import math

def calc_turbidity(a0: float, I90: float) -> float:
    """
    The function input is the Calibration constant and Ninety degree detector current and it returns calculated turbidity

    Args:
        a0: calibration constant
        I90: ninety degree detector current value
        
    Returns:
        The calculated turbidity (T)
    """
    
    return a0 * I90

def safe_Time(T0: float)-> float:
    """
    The function input is current turbidity and it returns hours elapsed until the water is safe

    Args:
        T0: current turbidity
        
        
    Returns:
        hours until water is safe
    """
    
    
    d = .02

    return (-1* math.log(T0))/ math.log(1-d)


def main():
    response = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    turb_data = response.json()['turbidity_data']

    turbidity = 0

    
    for i in range(5):
        current = turb_data[-i-1]

        turbidity += calc_turbidity(current['calibration_constant'], current['detector_current'])

    turbidity/= 5
    b = 0

    if (turbidity > 1):
        b = safe_Time(turbidity)
        print('Average turbidity based on most recent five measurements = %.4f NTU\nWarning: Turbidity is above threshold for safe use\nMinimum time required to return below a safe threshold = %.2f hours' % (turbidity, b))

    else:
        print('Average turbidity based on most recent five measurements = %.4f NTU\nInfo: Turbidity is below threshold for safe use\nMinimum time required to return below a safe threshold = %.2f hours' % (turbidity, b))
    

    
    
    


    




if (__name__ == '__main__'):
    main()