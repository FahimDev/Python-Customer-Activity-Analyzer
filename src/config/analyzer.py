
import json
import os
from dateutil import parser

import math

import pandas as pd


class Analyzer:

    __ignore_files =  ['README']    #List of ignorable file names at '/data' folder (keep file extension)

    def __init__(self, user_status, from_date, to_date):
        self.user_status = user_status
        self.from_date = from_date
        self.to_date = to_date


    def user_status_analyzer(self):
            # Redirecting according to the Command Type
            if self.user_status == 'active':
                self.__active()
            elif self.user_status == 'superactive':
                self.__superactive()
            elif self.user_status == 'bored':
                self.__bored()
            else:
                print("Status unknown!")

    #Absreaction(OOP) - Keeping all complex functionality private
    def __processor(self, context, dir_path, files):

        #Will Collect all user ID according to the Status Type
        target_user_id = []

        for file in files:
            
            #To Avoid unwanted files from reading
            if any(ig_f == file for ig_f in self.__ignore_files):
                continue

            #converting JSON files into Dictionary
            calendar = json.load(open(dir_path+file, encoding='utf-8'))

            days_details= calendar['calendar']['daysWithDetails']

            input_daterange = pd.date_range(parser.parse(self.from_date).date(), parser.parse(self.to_date).date())


            meal_count, user_id = self.__getMealCount(calendar, days_details, input_daterange)
            
            if user_id is not None and meal_count > context['meal_range_min'] and meal_count < context['meal_range_max'] and context['status'] != 'bored':

                target_user_id.append(user_id)

            elif context['status'] == 'bored' and user_id is not None:

                #Taking 1st date (starting date) from userID.json file
                user_start_date = list(calendar['calendar']['dateToDayId'].keys())[0]

                #Getting date range of PRECEDING PERIOD to check, if the user was ACTIVE in the past or not
                prev_daterange = pd.date_range(parser.parse(user_start_date).date(), parser.parse(self.from_date).date())

                meal_count, user_id = self.__getMealCount(calendar, days_details, prev_daterange)

                if user_id is not None and meal_count > context['meal_range_min'] and meal_count < context['meal_range_max']:

                    target_user_id.append(user_id)


        self.__printOutput(context, target_user_id)



    
    def __printOutput(self, context, userId_list):

        grammatical = 'Users are'

        if len(userId_list) < 2:
            grammatical = 'User is'
            
        print("\n")
        print('The ID list of {} {} given:"{}"'.format(context['status'], grammatical, userId_list))



    def __getMealCount(self,calendar, days_details, input_daterange):
        day_id_list = []
        meal_count = 0
        user_dates = calendar['calendar']['dateToDayId']

        for single_date in input_daterange:
            for user_date in user_dates.keys():
                if single_date.strftime("%Y-%m-%d") == user_date:
                    day_id_list.append(user_dates[user_date])

        
        for day_id in day_id_list:
            for day_detail_fk in days_details.keys():
                if str(day_id) == day_detail_fk:   
                    meal_count += len(days_details[day_detail_fk]['details']['mealsWithDetails'].keys())

        if meal_count != 0:
            user_id = days_details[str(day_id_list[0])]['day']['userId']
        else:
            user_id = None

        return meal_count, user_id



    def __find_files(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.replace("\src\config", "\data\\") 
        file_names = os.listdir(dir_path)
        return dir_path, file_names

#----------------------------------------------------------------------------------------

    def __active(self):
        
        context = {
            'status': 'active',
            'meal_range_min': 4,
            'meal_range_max': 11
        }

        path, files = self.__find_files()

        self.__processor(context, path, files)


    def __superactive (self):
        context = {
            'status': 'superactive',
            'meal_range_min': 11,
            'meal_range_max': math.inf
        }

        path, files = self.__find_files()

        self.__processor(context, path, files)

    def __bored (self):
        context = {
            'status': 'bored',
            'meal_range_min': 4,
            'meal_range_max': 11
        }

        path, files = self.__find_files()

        self.__processor(context, path, files)

    