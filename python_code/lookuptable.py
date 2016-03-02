import matplotlib.pyplot as plot
import numpy as np

RESOLUTION = 4096
ALPHA = 3.0 / 1024.0 * float(RESOLUTION/4)
BETA = 10.0 / 1024.0 * float(RESOLUTION/4)

regularization_1 = ALPHA
regularization_2 = BETA


controlParameter = 1500  # 0 ... RESOLUTION/2

lookUpTable = [0] * RESOLUTION

for i in range(0, RESOLUTION):
    _exponent = (ALPHA * np.power(controlParameter, (controlParameter * 1.2) / float(RESOLUTION/2)));
    _numerator = (RESOLUTION/2) + _exponent;
    _denominator = abs(i -(RESOLUTION/2)) + _exponent + BETA;
    
    _temporal = _numerator / _denominator;
    lookUpTable[i] = (_temporal * (i -(RESOLUTION/2))) + (RESOLUTION/2);

## THIS ONE WORKS
#for i in range(0, RESOLUTION):
#    gain = (RESOLUTION/2 + np.power(controlParameter, controlParameter / (RESOLUTION/2 / 1.2)) * regularization_1 ) / (abs(i - (RESOLUTION/2)) + np.power(controlParameter,  controlParameter / (RESOLUTION/2 / 1.2)) * regularization_1 + regularization_2);
#
#    lookUpTable[i] = (i - (RESOLUTION/2)) * gain + RESOLUTION/2



plot.plot(lookUpTable)
plot.grid()
#plot.xlim([-200, RESOLUTION + 200])
#plot.ylim([-200, RESOLUTION + 200])
plot.show()
