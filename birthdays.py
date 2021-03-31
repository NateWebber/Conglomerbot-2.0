#Important Note: in users.json, pronouns are stored in order [nominative, accusative/dative, genitive]

import json
import discord
import datetime
from datetime import date

data = None

with open("users.json", "r") as user_json:
    data = json.load(user_json)

def checkBirthday():
    print ("Starting a birthday check!")
    today = date.today()
    today_formatted = today.strftime("%m/%d/%y") #today in MM/DD/YY format
    today_no_year = today.strftime("%m/%d") #today in MM/DD format
    today_year = today.strftime("%Y") #the current year
    print(today_no_year)
    birthday_list = []
    for user in data["users"]:
        user_bday_full = user["birthday"]
        user_bday_no_year = user_bday_full[:-5]
        user_bday_year = user_bday_full[6:]
        print(user_bday_no_year)
        if today_no_year == user_bday_no_year:
            print("Detected that today is {name}'s birthday!".format(name = user["name"]))
            print(user["pronouns"][0])
            conjugated = conjugateToBe(user["pronouns"][0])
            print(conjugated)
            preformat_string = "Today is {name}'s birthday! {nom_pronoun} {conjugated_to_be} {age} years old today. Be sure to wish {acc_pronoun} a happy birthday!"
            return_string = preformat_string.format(name = user["name"], nom_pronoun = user["pronouns"][0].capitalize(), conjugated_to_be = conjugated, age = (int(today_year) - int(user_bday_year)), acc_pronoun = user["pronouns"][1])
            return return_string
    return None

def getBirthday(target):
    for user in data["users"]:
        if (user["discord_ping"]) == target or user["name"] == target:
            found_bday = user["birthday"]
            bday_obj = datetime.datetime.strptime(found_bday, '%m/%d/%Y')
            long_bday = bday_obj.strftime('%B %d')
            today = date.today()
            days_until_bday = calculateNextBirthday(bday_obj, datetime.datetime.now())
            return ("{name}'s birthday is {bday}. That will be in {days} day(s)!".format(name=user["name"], bday=long_bday, days=days_until_bday))
    return None

        

def conjugateToBe(pronoun):
    if (pronoun == "he" or pronoun == "she"):
        return "is"
    else:
        return "are"


def calculateNextBirthday(bday, today):
    delta1 = datetime.datetime(today.year, bday.month, bday.day)
    delta2 = datetime.datetime(today.year+1, bday.month, bday.day)

    return (((delta1 if delta1 > today else delta2) - today).days + 1)

