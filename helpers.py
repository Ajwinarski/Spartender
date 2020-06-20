from imports import *

##############################################
################## Helpers ###################
##############################################

class NewUser():
    
    def __init__(self, **kwargs):
        super(NewUserPopup, self).__init__(**kwargs)
        # namePopup = NamePopup(title='Enter your name')
        keypadPopup = KeypadPopup(title='Enter a pin')
        
    # First, open the normal keyboard and ask for the users first name (check to make sure the name isn't in the database!!!!)
    def open_name_popup(self):
        pass
    
    # Next, open the keypad and ask for the users 
    def open_keypad_popup(self):
        KeypadPopup.open()
        
class PinVerifier():
    
    def __init__(self, **kwargs):
        super(PinVerifier, self).__init__(**kwargs)
        # self.users = TinyDB('databases/users.json')
        
    # Returns:
    #    0 if no user found
    #    1 if only 1 user with that pin
    #    2 if more than 1 user with the same pin
    def verify(self, encoded):
        pass
        # Check if the pin is found
        # print("Encoded string: {0}".format(self.encoded))
        
        #####################
        # TODO: WORK ON THIS FIRST
        #####################
        
        # for dict in users:
        #     if dict['pin'] == encoded:
        #         print("Found match for {0}".format(encoded))
        
        
        # if users.contains(Users.user.pin == encoded):
        #     print("USER FOUND")
        #     if (users.count(Users.user.pin == encoded) > 1):
        #         # Require name to be entered
        #         print("MORE THAN ONE")
        
        # print(Users.field.matches(encoded))
        
        # print(users.search(Users.users.any(PinQuery.pin == encoded)))
        
        # self.users.all()
        
        # for item in self.users:
        #     print(item)
        
        # print(users.search(query.pin == self.encoded))
        # if (self.pin in users["pin"]):
        #     print("Pin found")
        #     # Count the number of occurances of a pin in the JSON
        #     for jsonObject in self.users:
        #         print(jsonObject["pin"])
                # if (jsonObject["pin"])
                
            # count = 
            # If more than one user with the same pin
            # if  
        
        # Return true if pin found
        # return self.pin in self.users
        

    # Check the Database for the entered pin
    def do_check_pin(self):
    # TODO: Check database for pin numbers

        # Used for transitioning to drinks page on successful pin
        if self.do_db_read() and self.popupType == 'drinks':

            # Set the users data to screen


            ### TODO: After a user enters in their pin, personalize their drinks menu with name and credits

            # Transition to drinks page
            sm.current = "drinks"

        # Used for transitioning to settings page on successful pin
        elif self.encodedStr == 'MTEzMA==' and self.popupType == 'settings':
            self._do_verification()

        # Clear the pinArray
        self.pinArray.clear()

        self.change_text('d', self.pin1Observer)
        self.change_text('d', self.pin2Observer)
        self.change_text('d', self.pin3Observer)
        self.change_text('d', self.pin4Observer)

        # Close the Popup
        self.dismiss()

        pass
    
# Gets the user database from csv file (NO LONGER BEING USED)
class csv_database():
    file = open(csvDB, 'a')
    rows = ['pin', 'name', 'credits']
    reader = csv.DictReader(file)
    writer = csv.DictWriter(file, fieldnames=rows)

    # If any data on a row is found, return the row
    def get_row(self, data):
        for row in self.reader:
            for item in row:
                if item == '{data}':
                    return row