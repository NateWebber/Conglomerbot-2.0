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
    birthday_list = []
    for user in data["users"]:
        user_bday_full = user["birthday"]
        user_bday_no_year = user_bday_full[:-5]
        user_bday_year = user_bday_full[6:]
        if today_no_year == user_bday_no_year:
            print("Detected that today is {name}'s birthday!".format(name = user["name"]))
            conjugated = conjugateToBe(user["pronouns"][0])
            preformat_string = "@everyone 🎂🎉🎈 Today is {name}'s birthday! {nom_pronoun} {conjugated_to_be} {age} years old today. Be sure to wish {acc_pronoun} a happy birthday! 🎂🎉🎈"
            return_string = preformat_string.format(name = user["name"], nom_pronoun = user["pronouns"][0].capitalize(), conjugated_to_be = conjugated, age = (int(today_year) - int(user_bday_year)), acc_pronoun = user["pronouns"][1])
            return return_string
    return None

def getBirthday(target):
    for user in data["users"]:
        if (user["discord_id"]) == target or user["name"] == target:
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

def getSoonestBirthday():
    days = 999
    closest_user = None
    for user in data["users"]:
        found_bday = user["birthday"]
        bday_obj = datetime.datetime.strptime(found_bday, '%m/%d/%Y')
        new_days = calculateNextBirthday(bday_obj, datetime.datetime.now())
        if new_days < days:
            days = new_days
            closest_user = user
    return ("{name}'s birthday is next on {bday}. That will be in {days} day(s)!".format(name=closest_user["name"], bday=datetime.datetime.strptime(closest_user["birthday"], '%m/%d/%Y').strftime('%B %d'), days=days))

