from math import log, sqrt

def rank(up, down, confidence=1.6):
    n = up + down
    if n == 0:
        return 0
    z = confidence # 1.0 is 85%, 1.6 is 95% confidence
    p = float(up)/n
    return round(p + z*z/(2*n) - z * sqrt((p*(1-p)+z*z/(4*n)) / (1 + z*z/n)), 6)
