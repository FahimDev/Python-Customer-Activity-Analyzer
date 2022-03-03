from .analyzer import Analyzer
from .validator import Validator
class Menu:
    __BANNER = """
    ---------------------------------------------------------------------------------------------------
    Welcomne to Chaldal se-coding-assignment - Hypothetical Menu Planning Calendar Application Analyzer 
    ---------------------------------------------------------------------------------------------------
    -This Analyzer is developed with Python (v3.10.0)
    -Developed  by Md. Ariful Islam (fahim.arif0373@outlook.com | ariful@ieee.org)
    ___________________________________________________________________________________________________
    
    """
    def __init__(self):
        print(self.__BANNER)
        self.options()


    def options(self):
        print("----------------------------------------MENU-------------------------------------------------------")
        #Current Task is the Default Option of Menu. If required we can use IF/ELSE for other Functions
        self.__findUserIdByStatus()
    


    def __findUserIdByStatus(self):
        # For being capable of accepting multiple commands 
        while True:
            print("Please provide your command and press ENTER:")
            print('[To turn off the app just type "exit app now" and press ENTER]')
            print("Command Template: Status StartDate EndDate")
            print("Date Format: YYYY-MM-DD (Example=> 2016-09-01)")
            print("\n")

            user_status, from_date, to_date =  list(map(str,input().split()))

            if all(param is not None for param in [user_status, from_date, to_date]):

                
                if user_status == 'exit':
                    print("Turning off app........")
                    break

                check = Validator
                check = check.startEndDate(from_date, to_date)
                #Checking Start and End Dates are Valid or not.... If Dates are Valid it will Return True.

                if check:
                    appObj = Analyzer(user_status, from_date, to_date)
                    appObj.user_status_analyzer()

                print("---------End---------")
                print("\n")
            else:

                print("Parameter Missing!")

