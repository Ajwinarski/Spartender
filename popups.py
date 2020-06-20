from imports import *
from helpers import *

##############################################
################### Popups ###################
##############################################

# Confirm drink selection popup
class DrinkPopup(Popup):

    drinkObserver = ObjectProperty()
    ingredientsObserver = ObjectProperty()
    doubleCheckboxObserver = ObjectProperty()
    # detailObserver = ObjectProperty()
    selectedDrink = ""
    ingredients = ""
    details = ""
    ingredientsArray = []
    l_ingredients = "Ingredients: "

    def on_pre_open(self):
        
        #TODO: If its a shot, add "shot" at the end of the drink observer string.
        #       In other words, customize the message based on the drink.
        self.drinkObserver.text = "Would you like to pour a {0}?\n".format(self.selectedDrink)
        self.ingredientsObserver.text = self.l_ingredients + "{0}\n".format(self.details)

    def pour_drink(self):
        print("Pouring a {0} double".format(self.selectedDrink) if self.doubleCheckboxObserver.active 
              else "Pouring a {0}".format(self.selectedDrink))
        for item in self.ingredientsArray:
            print(item)

        # TODO: Do the drink pouring for specific pumps here!!!

        self.dismiss()

    pass


# Enter new users name popup
class NamePopup(Popup):
    
    def __init__(self, **kwargs):
        super(NamePopup, self).__init__(**kwargs)
        
    pass

# New Keypad
class KeypadPopup(Popup):
    __events__ = ('on_verification', )
    
    pin1Observer = ObjectProperty()
    pin2Observer = ObjectProperty()
    pin3Observer = ObjectProperty()
    pin4Observer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(KeypadPopup, self).__init__(**kwargs)
        self.pinNums = 0
        self.pinArray = []
        self.user = 'User'
        self.credits = 9999
        self.pinsObserver = [
            self.pin1Observer,
            self.pin2Observer,
            self.pin3Observer,
            self.pin4Observer
        ]

    # Triggered: on_dismiss
    def on_dismiss(self):
        self.pinNums = 0
        self.pinArray.clear()

    # Call verification function?
    def _do_verification(self):
        self.dispatch('on_verification')

    # TODO: Can this method open different settings?
    def on_verification(self, *largs):
        config.update_config('austinSettings.py')
        pass

    # Logic for each pin pressed
    def do_pin_pressed(self, num):
        
        if commenting: print("Number ", num, " was pressed.")
        
        # Add pin to array
        self.pinArray.append(num)
        
        # Check for complete pin
        if (self.pinNums == 3):
            # Change the empty space to have a '*'
            self.pinsObserver[self.pinNums].text = '*\n'
            # Get the entered pin as a string
            enteredPin = ''.join(self.pinArray)
            # Get the encoded pin
            encodedPin = self.get_encoded_pin(enteredPin)
            
            self.check_pin(enteredPin, encodedPin)
            
            # TODO: RE_WRITE THE popupType to seperate classes
            # if self.popupType == 'create': self.do_db_insertion()
            # self.do_check_pin()
        else:
            self.pinsObserver[self.pinNums].text = '*\n'
            
        # Increment pinNums
        self.pinNums += 1
            
    # Deletes an entered pin
    def do_pin_deleted(self):
        
        # Return if the array is empty
        if not self.pinArray:
            return
        
        # Remove last pin from array, then increment pin nums
        self.pinArray.pop()
        # Decrement pinNums
        self.pinNums -= 1
        # Change the '*' back to ' '
        self.pinsObserver[self.pinNums].text = '____\n'
        # self.change_text('d', self.pinsObserver[self.pinNums])


    # Visualization of the number of entered pins
    def change_text(self, edit, observer):
        # If you are adding, put a star
        if edit == 'a':
            observer.text = '*\n'
        else:
            observer.text = '____\n'

    # Encodes the 4-digit pin
    # def do_pin_encoding(self):
    #     # Encode the entered pin
    #     encodedBytes    = base64.b64encode(self.enteredPin.encode("utf-8"))
    #     self.encodedStr = str(encodedBytes, "utf-8")
        
    # Encodes and returns the 4-digit pin
    def get_encoded_pin(self, pin):
        return str(base64.b64encode(pin.encode("utf-8")), "utf-8")

    # # Used to insert data in the Database
    # def do_db_insertion(self):
    #     # Open the database
    #     f = open(csvDB, 'a')

    #     # Define the items per line and make a writer
    #     rows = ['pin', 'name', 'credits']
    #     writer = csv.DictWriter(f, fieldnames=rows)

    #     # Write the information to the file
    #     # writer.writeheader()      # Writes the fieldnames to top of file
    #     writer.writerow({'pin'    : self.encodedStr,
    #                      'name'   : self.user,
    #                      'credits': self.credits})

    # Used to check for a pin in the Database
    # def do_db_read(self):
    #     # Open the database
    #     f = open(csvDB, 'r')

    #     # Search the file for the pin
    #     with f:
    #         reader = csv.DictReader(f)
    #         for row in reader:
    #             if row['pin'] == self.encodedStr:
    #                 # print(row['pin'][:-2])
    #                 global currentUserName
    #                 currentUserName = row['name']
    #                 App.loggedInUserName = row['name']
    #                 global currentUserCredits
    #                 if row['credits'] == "9999":
    #                     currentUserCredits = '∞'
    #                     App.loggedInUserCredits = '∞'
    #                 else:
    #                     currentUserCredits = str(row['credits'])
    #                     App.loggedInUserCredits = str(row['credits'])
    #                 return True
    #         return False
    #     pass

    # Write the current users info to be used in the session
    # def set_user_info(self, name, credits):
    #     # Write the current users info to be used during the session
    #     self.userInfo = [name, credits]
    
    def check_pin(self, pin, encoded):
        verifier = PinVerifier()
        
        verifier.verify(encoded)

        # Used for transitioning to drinks page on successful pin
        # if self.do_db_read() and self.popupType == 'drinks':

            ### TODO: After a user enters in their pin, personalize their drinks menu with name and credits

            # Transition to drinks page
            # sm.current = "drinks"

        # Used for transitioning to settings page on successful pin
        # elif self.encodedStr == 'MTEzMA==' and self.popupType == 'settings':
        #     self._do_verification()

        # Clear the pinArray
        self.pinArray.clear()

        self.change_text('d', self.pin1Observer)
        self.change_text('d', self.pin2Observer)
        self.change_text('d', self.pin3Observer)
        self.change_text('d', self.pin4Observer)

        # Close the Popup
        self.dismiss()

        pass

    # Check the Database for the entered pin
    # def do_check_pin(self):
    # # TODO: Check database for pin numbers

    #     # Used for transitioning to drinks page on successful pin
    #     if self.do_db_read() and self.popupType == 'drinks':

    #         # Set the users data to screen


    #         ### TODO: After a user enters in their pin, personalize their drinks menu with name and credits

    #         # Transition to drinks page
    #         sm.current = "drinks"

    #     # Used for transitioning to settings page on successful pin
    #     elif self.encodedStr == 'MTEzMA==' and self.popupType == 'settings':
    #         self._do_verification()

    #     # Clear the pinArray
    #     self.pinArray.clear()

    #     self.change_text('d', self.pin1Observer)
    #     self.change_text('d', self.pin2Observer)
    #     self.change_text('d', self.pin3Observer)
    #     self.change_text('d', self.pin4Observer)

    #     # Close the Popup
    #     self.dismiss()

    #     pass

    # pass