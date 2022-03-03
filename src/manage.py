"""command-line utility for analyze app."""

from config.menu import Menu

def main():


    try:
        menuObj = Menu()

        menuObj

    except Exception as e:
        
        print("Something went wrong! Error:")
        print(e)
        #If any Error occur in other classes those Exceptions will be also printed here.


if __name__ == '__main__':
    main()