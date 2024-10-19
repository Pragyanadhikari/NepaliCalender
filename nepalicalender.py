# Write a
# python module called “Nepali Calendar”. Your module should be able to show
# nepali date,day, time, tithi(तिथि) and important event like (लोकतन्त्र दिवस , आमाको मुख हेर्ने दिन , हरितालिका तीज , संबिधान दिवस , फूलपाती, ग्याल्बो लोसार, विश्व पर्यटन दिवस , विश्व मजदुर दिवस) etc... when you give english date as input.



import calendar
import datetime
tithi1=['Pratipada','Dwitiya','Tritiya','Panchami','Sasti','Saptami','Aastami','Nawami','Dashami','Ekadasi','Dwadashi','Tryodashi','Chaturdashi','Aausi']
tithi2=['Pratipada','Dwitiya','Tritiya','Panchami','Sasti','Saptami','Aastami','Nawami','Dashami','Ekadasi','Dwadashi','Tryodashi','Chaturdashi','Purnima']
user_input_date=input("Enter english date in format (YYYY-MM-DD) : ")
yy=int(user_input_date[:4])
mm=int(user_input_date[5:7])
dd=int(user_input_date[8:])
print("Given english date :\n ",calendar.month(yy,mm))

def year_conversion(yy,mm,dd):
    if mm>4 or (mm==4 and dd>=15):
        nepali_yy=yy+57
    else:
        nepali_yy=yy+58
    return nepali_yy
def month_conversion(mm,dd):
    if dd > 15:
        nepali_mm = mm - 3 
    else:
        nepali_mm = mm - 4 
    if nepali_mm <= 0:
        nepali_mm += 12  
    return nepali_mm
def day_conversion(dd):
    if dd > 15:
        nepali_day = dd - 15
    else:
        nepali_day = dd + 15 
    return nepali_day
def calculate_tithi(np_year, np_month, np_day):
    # Reference Nepali date: Nepali calendar starts from 2081-07-02
    reference_nepali_date = datetime.datetime(2081, 7, 2)
    
    # Converted Nepali date from input (note we use datetime.datetime here)
    nepali_date = datetime.datetime(np_year, np_month, np_day)
    
    # Calculate the difference in days between the reference and the given Nepali date
    day_difference = abs((nepali_date - reference_nepali_date).days)
    
    # Determine the Tithi cycle
    tithi_index = day_difference % len(tithi1)
    tithi_cycle = (day_difference // 15) % 2  # Alternating cycles of 15 days

    if tithi_cycle == 0:
        return tithi1[tithi_index]
    else:
        return tithi2[tithi_index]
np_year=year_conversion(yy,mm,dd)
np_month=month_conversion(mm,dd)
np_day=day_conversion(dd)
print("Nepali year : ",np_year)
print("Nepali month:",np_month)
print("Nepali day: ",np_day)
print('Thiti is: ',calculate_tithi(np_year,np_month,np_day))
current_time=datetime.datetime.now()
print("Current time is: {}".format(current_time.strftime("%H:%M:%S")))