from dateutil import parser

class Validator:

    def startEndDate(start_date, end_date):
        if parser.parse(start_date).date() < parser.parse(end_date).date():
            return True
        else:
            print ("From-date is greater than To-date!")