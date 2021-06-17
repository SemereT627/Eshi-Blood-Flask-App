from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.fromisoformat(d1)
    d2 =datetime.fromisoformat(d2)
    return abs((d2 - d1).days)
def minutes_between(d1,d2):
    d1 = datetime.fromisoformat(d1)
    d2 =datetime.fromisoformat(d2)
    return abs(((d2 - d1).seconds))%3600/60