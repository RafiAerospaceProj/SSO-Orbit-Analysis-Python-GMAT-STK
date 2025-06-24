from math import pi

def sma_from_revs_per_day(revs_per_day, mu=398600.4418 ):# km^3/s^2
    
    T = 86400 / revs_per_day  # seconds per rev
    a = (mu * T**2 / (4 * pi**2))**(1/3)
    return a  # in km

sma = sma_from_revs_per_day(14)  # ~7478.1 km