from datetime import datetime, date, timedelta
import main
def current_time_date():

    today_time = datetime.now().strftime("%H:%M:%S")
    today = date.today()
    date_list = []
    for i in range(3):
         date_list.append(today + timedelta(days=i))
    return today_time, date_list


def date_time_availability(theatre):
    theatre = theatre
    t = []
    data_date = main.records.find_one({"theatre": theatre})
    for x in data_date["dates"]:
        t.append(x)
    return t

def upadte_date_time(theatre):
    theatre = theatre
    result = current_time_date()
    today_time = result[0]
    date_list = []
    for i in result[1]:
        date_list.append(str(i))

    dates  = date_time_availability(theatre)

    new_value = {"$unset": {}, "$set": {}}


    for value in dates:
        if value not in date_list:
            set_value = "dates." + value
            new_value["$unset"][set_value] = ""
        if value == date_list[0]:
            if str(today_time) >= "10":
                morning = "dates." + value + ".timings.morning_show"
                new_value["$unset"][morning] = ""
            if str(today_time) >= "17":
                evening = "dates." + value + ".timings.evening_show"
                new_value["$unset"][evening] = ""


    for value in date_list:
        if value not in dates:
            set_value = "dates."+value
            new_value["$set"][set_value] = { "timings" : {
                                "morning_show" :{"seat availability": 20},
                                "evening_show" : {"seat availability": 20}
                            }}





    main.records.update_one({"theatre": theatre}, new_value)

def update_all_theatres():
    theatre_data = main.records.find()
    for x in theatre_data:
        y = x["theatre"]
        upadte_date_time(y)

def booking_update(cinemas,date, show, number):
    num = number
    new_value = {"$unset": {}, "$set": {}}
    if num > 0:
        show_times = "dates." + date + ".timings." + show + ".seat availability"
        new_value["$set"][show_times] = num
    else:
        show_times = "dates." + date + ".timings." + show
        new_value["$set"][show_times] = 0
    main.records.update_one({"theatre": cinemas}, new_value)





