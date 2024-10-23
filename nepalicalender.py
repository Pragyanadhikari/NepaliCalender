# Write a
# python module called “Nepali Calendar”. Your module should be able to show
# nepali date,day, time, tithi(तिथि) and important event like (लोकतन्त्र दिवस , आमाको मुख हेर्ने दिन , हरितालिका तीज , संबिधान दिवस , फूलपाती, ग्याल्बो लोसार, विश्व पर्यटन दिवस , विश्व मजदुर दिवस) etc... when you give english date as input.



import calendar
import datetime
import ephem
import csv
import requests

tithi=["प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी", "अष्टमी",
    "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा","प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी", "अष्टमी",
    "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "अमावस्या"]
days={"Sunday":"आइतबार",
      "Monday":"सोमबार",
      "Tuesday": "मंगलबार",
      "Wednesday": "बुधबार",
      "Thursday": "बिहीबार",
      "Friday": "शुक्रबार",
      "Saturday": "शनिबार"
    }
Important_event = {
    (1, 1): "नयाँ वर्ष",  
    (1, 11): "लोकतन्त्र दिवस", 
    (1, 18): "विश्व मजदुर दिवस",
    (1, 30): "श्रीपञ्चमी",
    (3, 8): "महिला दिवस",
    (6, 3): "संबिधान दिवस", 
    (7, 1): "विश्व पर्यटन दिवस", 
    (9, 7): "उधौली पर्व",  
    (9, 12): "मोहनी नख",  
    (9, 15): "अन्नपूर्ण यात्रा",  
    (10, 1): "माघे संक्रान्ति",  
    (11, 7): "प्रजातन्त्र दिवस",
}


def load_days_in_month(csv_path):
    with open(csv_path, "r") as file:
        month_data = {}
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            year = int(row[0])
            month_days = list(map(int, row[1:]))
            month_data[year] = month_days
    return month_data
path = "calendar_bs.csv"
bs_month_days = load_days_in_month(path)
def convert_to_bs(eng_year, eng_month, eng_day, bs_month_days):
    #Adding reference date for english and nepali
    ref_ad = datetime.date(1944, 1, 1) 
    ref_bs = (2000, 9, 17) 
    ref_day = calendar.SATURDAY
    
    given_date = datetime.date(eng_year, eng_month, eng_day)
    days_diff = (given_date - ref_ad).days

    bs_year, bs_month, bs_day = ref_bs
    day_count = ref_day

    while days_diff != 0:
        days_in_current_month = bs_month_days[bs_year][bs_month - 1]
        bs_day += 1
        if bs_day > days_in_current_month:
            bs_month += 1
            bs_day = 1
        if bs_month > 12:
            bs_year += 1
            bs_month = 1

        day_count = (day_count + 1) % 7
        days_diff -= 1

    return f"{bs_year}-{bs_month}-{bs_day}", calendar.day_name[day_count]

def get_event(bs_year, bs_month, bs_day):
    if (bs_month, bs_day) in Important_event:
        return Important_event[(bs_month, bs_day)]
    else:
        return "No event"
    
def create_nepali_calendar(year, month, bs_month_days):
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    months = ["Baishakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin", "Kartik", 
              "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"]

    days_in_month = bs_month_days[year][month - 1]

    ad_month_map = {1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 1, 11: 2, 12: 3}
    ad_month = ad_month_map[month]
    ad_year = year - 57 if ad_month > 3 else year - 56

    first_nep_date = convert_to_bs(ad_year, ad_month, 27, bs_month_days)
    first_nep_day = first_nep_date[0].split("-")[2]
    start_day = first_nep_date[1][:3]
    
    day_idx = weekdays.index(start_day)
    day_list = [" "] * day_idx

    for i in range(1, int(days_in_month) + 1):
        day_list.append(str(i))
    calendar_lines = []
    calendar_lines.append(f"{months[month - 1]} {year}".center(29))
    calendar_lines.append(" ".join(weekdays))
    
    for i in range(0, len(day_list), 7):
        calendar_lines.append(" ".join(day_list[i:i + 7]))
    
    return "\n".join(calendar_lines)

def current_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        location = response.json()['loc'].split(',')
        return location[0], location[1]
    except Exception:
        raise ValueError("Unable to retrieve location.")
    
def calculate_tithi(observation_date):
    latitude, longitude = get_location()
    
    observer = ephem.Observer()
    observer.lat, observer.lon = latitude, longitude
    observer.date = ephem.Date(observation_date)
    new_moon = ephem.previous_new_moon(observer.date)
    lunar_age = observer.date - new_moon
    
    current_tithi = int(lunar_age * 30 / 29.53) + 1
    return f"{tithi[current_tithi - 1]}"

def get_nepali_details(eng_year, eng_month, eng_day):
    bs_date, bs_day = convert_to_bs(eng_year, eng_month, eng_day, bs_month_days)
    bs_day = days[bs_day]
    event_name = get_event(eng_year, eng_month, eng_day)
    
    return {
        "Nepali Date": bs_date,
        "Day": bs_day,
        "Current Time": current_time(),
        "Tithi": calculate_tithi(datetime.date(eng_year, eng_month, eng_day)),
        "Event": event_name
    }



