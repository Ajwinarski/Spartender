import kivy
import json
import base64
import random
import csv
from kivy import require
# from tinydb import TinyDB, Query

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import Settings
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.widget import Widget

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.factory import Factory
from kivy.metrics import dp, sp
from kivy.properties import *

# Imports the json settings
from settingsjson import settings_json, users_json
from functools import partial

# Define the config parser for settings
config = ConfigParser()

# Define the Database

# Define the Screen Manager
sm = ScreenManager(transition = SlideTransition(duration = 0.70))

# Globals
green = (0.09411,0.270588,0.231372,1)   #rgba(24,69,59,1) / 255 (Forest Green)
white = (1,1,1,1)                       #rbga(0,0,0,1)
currentUserName = ''                    # Current user name
currentUserCredits = 0                  # Current user credits

# Set the window color and to fullscreen without the top menu
from kivy.core.window import Window
Window.size = (800, 480)
Window.borderless = True
Window.clearcolor = green

# Mark as true to see wha the program is doing in detail
commenting = False

class MyKeyboardListener(Screen):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
                            self._keyboard_close, self, 'text')

        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            vkeyboard = self._keyboard.widget

            # Define the keyboard layout
            vkeyboard.layout = 'numeric.json'
            vkeyboard.size_hint = (.65,.4)
            vkeyboard.pos_hint_x = .5

        if commenting:
            for layout in vkeyboard.available_layouts:
                print(layout)

        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        pass

    def _keyboard_close(self):
        print('Keyboard closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'has been pressed')
        print(' - text is %r' % keycode[1])
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    pass

class LongpressButton(Factory.Button):

    __events__ = ('on_long_press', )

    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def do_request_pin(self):
        KeypadPopup(title='Enter your pin').open()

""" Screen Definitions """

class MainScreen(Screen):

    settingsImage = ObjectProperty()
    drinksImage   = ObjectProperty()
    configImage   = ObjectProperty()

    # Darkens button color on click
    def do_pressed(self, button, imagePath):
        if button == 's': self.settingsImage.source = imagePath
        elif button == 'd': self.drinksImage.source = imagePath
        else: self.configImage.source = imagePath
        if commenting: print("Pressed")

    # Lightens button color on release
    def do_released(self, button, imagePath):
        if button == 's': self.settingsImage.source = imagePath
        elif button == 'd': self.drinksImage.source = imagePath
        else: self.configImage.source = imagePath
        if commenting: print("Released")

    # Shows pin popup for drinks
    def show_pin_popup(self, type = 'drinks'):
        popup = KeypadPopup(title='Enter your pin')
        popup.popupType = type
        popup.open()

    def goto_drinks(self):
        if (int(App.get_running_app().config.get('settings','pinmode'))):
            self.show_pin_popup()
        else:
            sm.current = "drinks"
    pass

class DrinksScreen(Screen):

    nameText    = ObjectProperty(None, allownone=True)
    creditsText = ObjectProperty(None, allownone=True)

    def on_pre_enter(self):
        self.updateWelcomeMessages()

    def updateWelcomeMessages(self):
        # if username is not an empty string
        if currentUserName:
            curName = currentUserName
            potentialNameResponses = [f'{curName}',f'Drink up, {curName}',
                f'Essketit, {curName}', f'Welcome, {curName}', f'Drink Responsibly, {curName}']
            credT = f'Credits: {currentUserCredits}'
            self.updateText(random.choice(potentialNameResponses), credT)
        pass

    def updateText(self, nameT, creditsT):
        self.nameText.text = nameT
        self.creditsText.text = creditsT
        pass

    pass

class ConfigScreen(Screen):

    vodkaSlider = NumericProperty()
    rumSlider   = NumericProperty()
    soda1Slider = NumericProperty()
    soda2Slider = NumericProperty()

    pass

class MixedDrinksScreen(Screen):

    # view = ObjectProperty(None)
    #
    # def __init__(self, **kwargs):
    #     super(MixedDrinksScreen, self).__init__(**kwargs)
    #     Clock.schedule_once(self.create_scrollview)
    #
    # def create_scrollview(self, dt):
    #     base = ["element {}".format(i) for i in range(40)]
    #     layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    #     layout.bind(minimum_height=layout.setter("height"))
    #
    #     for element in base:
    #         layout.add_widget(Button(text=element, size=(50, 50), size_hint=(1, None),
    #                                  background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
    #     scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
    #     scrollview.add_widget(layout)
    #     self.view.add_widget(scrollview)


    # def __init__(self, **kwargs):
    #     super(MixedDrinksScreen, self).__init__(**kwargs)
    #
    #     scrollView = ScrollView(size_hint = (.8, 1))
    #     drinkData = RecycleView(data = [{'text': str(x),'size_hint':(1,None)} for x in range(20)],
    #                             viewclass = 'Button')
    #
    #     scrollView.add_widget(drinkData)
    #     self.add_widget(scrollView)
    pass

class ShotsDrinksScreen(Screen):
    pass

class SodaDrinksScreen(Screen):
    pass

class DrinkListView(RecycleView):
    def __init__(self, **kwargs):
        super(DrinkListView, self).__init__(**kwargs)
        self.data = [{'text': str(x),'size_hint':(1,None)} for x in range(20)]

class KeypadPopup(Popup):
    __events__ = ('on_verification', )

    pin1Observer = ObjectProperty()
    pin2Observer = ObjectProperty()
    pin3Observer = ObjectProperty()
    pin4Observer = ObjectProperty()
    popupType = 'drinks'
    enteredPin = ""
    encodedStr = ""
    user = "name"
    credits = 0
    pinNums = []

    def _do_verification(self):
        self.dispatch('on_verification')

    def on_verification(self, *largs):
        pass

    # Logic for each pin pressed
    def do_pin_pressed(self, num):

        self.pinNums.append(num)

        if commenting: print("Number", num, "was pressed")

        # Add the stars based on how many pins have been entered
        if len(self.pinNums) == 1:
            self.change_text('a', self.pin1Observer)
        elif len(self.pinNums) == 2:
            self.change_text('a', self.pin2Observer)
        elif len(self.pinNums) == 3:
            self.change_text('a', self.pin3Observer)
        elif len(self.pinNums) == 4:
            self.change_text('a', self.pin4Observer)
            self.enteredPin = ''.join(self.pinNums)
            self.do_pin_encoding()
            if self.popupType == 'create': self.do_db_insertion()
            self.do_check_pin()


    # Visualization of the number of entered pins
    def change_text(self, func, observer):

        if func == 'a':
            observer.text = '*'
        else:
            observer.text = '____'

    # Encodes the 4-digit pin
    def do_pin_encoding(self):
        # Encode the entered pin
        encodedBytes    = base64.b64encode(self.enteredPin.encode("utf-8"))
        self.encodedStr = str(encodedBytes, "utf-8")

    # Deletes an entered pin
    def do_pin_deleted(self):

        self.pinNums = self.pinNums[:-1]

        # Remove the stars based on how many pins have been entered
        if len(self.pinNums) == 0:
            self.change_text('d', self.pin1Observer)
        elif len(self.pinNums) == 1:
            self.change_text('d', self.pin2Observer)
        elif len(self.pinNums) == 2:
            self.change_text('d', self.pin3Observer)
        elif len(self.pinNums) == 3:
            self.change_text('d', self.pin4Observer)

    # Used to insert data in the Database
    def do_db_insertion(self):
        # Open the database
        f = open('database.csv', 'a')

        # Define the items per line and make a writer
        rows = ['pin', 'name', 'credits']
        writer = csv.DictWriter(f, fieldnames=rows)

        # Write the information to the file
        # writer.writeheader()      # Writes the fieldnames to top of file
        writer.writerow({'pin'    : self.encodedStr,
                         'name'   : self.user,
                         'credits': self.credits})

    # Used to check for a pin in the Database
    def do_db_read(self):
        # Open the database
        f = open('database.csv', 'r')

        # Search the file for the pin
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['pin'] == self.encodedStr:
                    # print(row['pin'][:-2])
                    global currentUserName
                    currentUserName = row['name']
                    global currentUserCredits
                    currentUserCredits = row['credits']
                    return True
            return False
        pass

    # Write the current users info to be used in the session
    # def set_user_info(self, name, credits):
    #     # Write the current users info to be used during the session
    #     self.userInfo = [name, credits]

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

        # Reset the pinNums string
        self.pinNums.clear()

        self.change_text('d', self.pin1Observer)
        self.change_text('d', self.pin2Observer)
        self.change_text('d', self.pin3Observer)
        self.change_text('d', self.pin4Observer)

        # Close the Popup
        self.dismiss()

        pass

    pass

# Screen Manager Definition
# class ScreenManager(ScreenManager):
#     def __init__(self, **kwargs):
#         return super(ScreenManager, self).__init__(**kwargs)

# Load the main menu .kv file
# presentation = Builder.load_file("spartender.kv")

class SpartenderApp(App):

    # screen_names = ListProperty([])
    # sm = ScreenManager(transition = SlideTransition(duration = 0.55))

    primary = green
    secondary = white

    # keyboard = Popup(title='Enter Your Pin',
    #     content=Button(text='1'),
    #     size_hint=(None, None), size=(360, 360))

    # Info for the Settings config
    def build_config(self, config):

        # Initialize the Settings tab
        config.setdefaults('settings', {
            'partyMode': False,
            'pinMode': True,
            'darkMode': True})
            # 'numericexample': 10,
            # 'optionsexample': 'option2',
            # 'stringexample': 'some_string',
            # 'pathexample': '/some/path'

        # Initialize the Users tab
        config.setdefaults('users', {
            'entername': '',
            'enterpin': False,
            'userslist': ''})

    # Add the Settings pages
    def build_settings(self, settings):

        settings.add_json_panel('General',
                                self.config,
                                data=settings_json)
        settings.add_json_panel('Users',
                                self.config,
                                data=users_json)
        # Use this is modify the settings appearance
        # settings.pos_hint = ({"right": 1, "center_y": .5})
        # settings.size_hint = (0.9, 0.9)
        pass

    # Setup the Settings and Pages
    def build(self):
        # FIX THE SETTINGS PANEL SO THAT THERE IS A quit()
        Setter = SettingsWithSidebar
        # keypad_Popup = KeypadPopup()

        # button1 = Button(text = 'YOYOYOYO')
        # Setter.add_interface(button1)

        self.settings_cls = Setter
        # self.add_kivy_panel()

        # self.settings_cls = SettingsWithSidebar
        # self.settings_cls.add_widget(self, button1)
        # self.settings.add_interface(self)
        self.use_kivy_settings = False

        # Menu Pages
        mainPage = MainScreen(name = "main")
        drinksPage = DrinksScreen(name='drinks')
        configPage = ConfigScreen(name='config')

        # Drinks Pages
        mixedDrinksPage = MixedDrinksScreen(name='mixedDrinks')
        shotsDrinksPage = ShotsDrinksScreen(name='shotsDrinks')
        sodaDrinksPage = SodaDrinksScreen(name='sodaDrinks')

        # Additional Pages
        self.keypadPage = KeypadPopup()

        # Make the global Screen Manager
        self.sm = sm

        # Add the screen widgets

        # # Main screen pages
        # self.sm.add_widget(mainPage)
        # self.sm.add_widget(drinksPage)
        # self.sm.add_widget(configPage)
        #
        # # Drinks screen pages
        # self.sm.add_widget(mixedDrinksPage)
        # self.sm.add_widget(shotsDrinksPage)
        # self.sm.add_widget(sodaDrinksPage)

        # Main screen pages
        sm.add_widget(mainPage)
        sm.add_widget(drinksPage)
        sm.add_widget(configPage)

        # Drinks screen pages
        sm.add_widget(mixedDrinksPage)
        sm.add_widget(shotsDrinksPage)
        sm.add_widget(sodaDrinksPage)

        # Additional screens
        # self.sm.add_widget(keypadPage)

        # # Set the first page to be main
        # self.sm.current = "main"

        # Set the first page to be main
        sm.current = "main"

        return self.sm

    # Hides the given widget from the view
    def hideWidget(self, wid, hide):

        if hide:
            wid.opacity, wid.disabled = 0, True
        elif not hide:
            wid.opacity, wid.disabled = 1, False
        pass

    # Swap the primary and secondary colors
    def changeColorMode(self, wid, _color):

        for item in wid:
            item.color = _color
        # Swaps the primary and secondary colors
        # self.primary, self.secondary = self.secondary, self.primary
        # colorObject.color = self.primary
        pass

    # Triggered when a setting has been changed
    def on_config_change(self, config, section, key, value):

        if config is self.config:
            token = (section, key)

            # Logic for Party Mode
            if token == ('settings', 'partyMode'):
                # Define the screen(s) and button(s) you want to hide
                mainScreen = self.sm.get_screen('main')
                configWid = mainScreen.ids.configBtn
                settingsWid = mainScreen.ids.settingsBtn
                drinksButton = mainScreen.ids.drinksBtn
                drinksImage = mainScreen.ids.drinksImg
                widgets = [configWid, settingsWid]

                # Call the function to hide config button here
                for wid in widgets:
                    self.hideWidget(wid, int(value))

                if int(value):
                    drinksButton.size_hint = (.9, 45)
                    drinksImage.source = './assets/design/DrinksBtnLarge.PNG'
                else:
                    drinksButton.size_hint = (.38, .45)
                    drinksImage.source = './assets/design/DrinksBtn.PNG'

                # Used to check the partyMode value in our .ini file
                # print(config.get('settings', 'partyMode'))
                pass


            # Logic for Pin Mode

            # Logic for dark Mode
            elif token == ('settings', 'darkMode'):

                widgets = []
                # List the pages and items on those pages
                # that need to be changed here

                ## Main Screen widgets
                mainScreen = self.sm.get_screen('main')
                titleLabel = mainScreen.ids.title
                # quitButton =
                # widgets.append(titleLabel)

                ## Drink Screen widgets
                drinksScreen = self.sm.get_screen('drinks')
                nameLabel = drinksScreen.ids.nameTxt
                # widgets.append(nameLabel)

                ## Drink Screen widgets
                configScreen = self.sm.get_screen('config')
                vodkaLabel = configScreen.ids.label_vodka_value
                rumLabel = configScreen.ids.label_rum_value
                soda1Label = configScreen.ids.label_soda1_value
                soda2Label = configScreen.ids.label_soda2_value
                widgets = [titleLabel, nameLabel, vodkaLabel,
                            rumLabel, soda1Label, soda2Label]

                if int(value):
                    self.changeColorMode(widgets, self.secondary)
                    Window.clearcolor = self.primary

                else:
                    self.changeColorMode(widgets, self.primary)
                    Window.clearcolor = self.secondary

            # Logic for new users entering there pins
            elif token == ('users', 'enterpin'):

                if int(value):
                    config.set('users', 'enterpin', False)
                    name = config.get('users', 'entername')
                    settingsPin = KeypadPopup(title='Enter your pin')
                    settingsPin.popupType = 'create'
                    if name is not 'name':
                        settingsPin.user = name
                    settingsPin.open()


if __name__ == '__main__':
    SpartenderApp().run()
