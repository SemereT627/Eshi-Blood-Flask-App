from datetime import date, datetime
import re
from eshiBlood.models.models import *
from eshiBlood import app, bcrypt, db
from dateutil.relativedelta import relativedelta
import datetime


def isValidEmail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    queriedEmail = UserCredential.query.filter_by(Email=email).first()
    if(queriedEmail != None and re.search(regex,email)):
        return True
    else:
        return False


def isValidPassword(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if(mat):
        return True
    else:
        return False


def isValidUserName(username):
    queiriedUserName = User.query.filter_by(UserName=username).first()
    if(queiriedUserName != None):
        return False
    else:
        return True





def isValidBirthdDate(birthdate):
    try:
        format_str = '%d/%m/%Y'  # The format
        birthdateObj = datetime.datetime.strptime(birthdate, format_str)
        difference = relativedelta(date.today(), birthdateObj).years
        if(difference >= 16):
            return True
        else:
            return False
    except:
        return False


def isValidGender(gender):
    if(gender == "Male" or gender == "Female"):
        return True
    else:
        return False


def isValidFirstName(firstname):
    if(re.match("^[a-zA-Z0-9_.-]+$", firstname)):
        return True
    else:
        return False
def timeStampToUtc(timestamp):
    tsList = timestamp.split(" ")[0].split("-")
    tsYear = int(tsList[0])
    tsMonth = int(tsList[1])
    tsDay = int(tsList[2])
    return datetime.datetime(
            year=tsYear, month=tsMonth, day=tsDay)

def differenceInMonths(startDate, endDate):
    """Calculates months between two datetime objects
    
    Keyword arguments:
    startDate -- timestamp string
    endDate -- timestamp string
    Return: number of months
    """
    
    try:
        
        
        start_date = timeStampToUtc(startDate)
        end_date = timeStampToUtc(endDate)
        difference = (end_date.year - start_date.year) * \
            12 + (end_date.month - start_date.month)
        return difference
    except:
        return 0

def isValidAppointment(appointment):
    """Used To check if an appointment satisfies donation ethics
    
    Keyword arguments:
    appointment -- Appointment Object with CreatedDate set to datetime.datetime.now()
    Return: Boolean
    """
    
    queriedAppointment = Appointment.query.filter_by(
        User=appointment.User).order_by(desc(Appointment.UpdatedAt)).first()
    if(queriedAppointment == None):
        return True
    else:
        lastTimeDonatedDate = queriedAppointment.UpdatedAt
        

        if(differenceInMonths(appointment.UpdatedAt,str(datetime.datetime.now()))<3):# TODO change timestamp without time zone to date
            return False
        else:
            return True


