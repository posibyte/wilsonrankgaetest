from datetime import datetime, timedelta
from math import log, sqrt

epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
    """ Return number of seconds from the epoch """
    today = date - epoch
    return today.days * 86400 + today.seconds + (float(today.microseconds) / 1000000)

def rank(up, down, confidence=1.6):
    n = up + down
    if n == 0:
        return 0
    z = confidence # 1.0 is 85%, 1.6 is 95% confidence
    p = float(up)/n
    return round(p + z*z/(2*n) - z * sqrt((p*(1-p)+z*z/(4*n)) / (1 + z*z/n)), 6)