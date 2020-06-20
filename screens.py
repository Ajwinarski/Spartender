from imports import *
from popups import *

##############################################
################## Screens ###################
##############################################

### Main Menu
class MainScreen(Screen):

    settingsImage = ObjectProperty()
    drinksImage   = ObjectProperty()
    configImage   = ObjectProperty()

    # Fired when you enter this screen
    def on_enter(self):
        # Clear user session (if not on initial startup)
        pass

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
        popup = KeypadPopup()
        popup.popupType = type
        popup.open()

    #   If: Pinmode is checked, trigger pin popup
    # Else: Go directly to drinks menu
    def goto_drinks(self):
        #   If: The pinmode settings checkbox is true
        # Else: Go straight to drinks screen
        if (int(App.get_running_app().config.get('settings','pinmode'))):
            self.show_pin_popup()
        else:
            sm.current = "drinks"

    pass

### Drink Screen
class DrinksScreen(Screen):

    nameText    = ObjectProperty(None, allownone=True)
    creditsText = ObjectProperty(None, allownone=True)

    # Before entering the screen...
    def on_pre_enter(self):
        self.updateWelcomeMessages()
        App.get_running_app().loggedInUserCredits = currentUserCredits

    # Set the user name label based on logged in user
    def updateWelcomeMessages(self):
        # Checks if username is not an empty string
        if currentUserName:
            self.getMessages(currentUserName)
        else:
            self.getMessages('User')
        pass

    # Used to get the upper left label quips
    def getMessages(self, name):
        potentialNameResponses = [f'{name}',f'Drink up, {name}',
            f'Essketit, {name}', f'Welcome, {name}',
            f'Drink Responsibly, {name}', f'Time to PEAK, {name}',
            f'Yeet, {name}']
        credT = f'Credits: {currentUserCredits}'
        self.updateText(random.choice(potentialNameResponses), credT)

    # Sets the name and credits based on signed in user
    def updateText(self, nameT, creditsT):
        self.nameText.text = nameT
        self.creditsText.text = creditsT
        pass

    # Deletes the current users session data
    def on_exit(self):
        global currentUserName
        currentUserName = ''
        self.updateText('', '')

    pass

### Configuration Screen
class ConfigScreen(TabbedPanel, Screen):

    # vodkaSlider = NumericProperty()
    vodkaSlider = ObjectProperty()
    # rumSlider   = NumericProperty()
    # soda1Slider = NumericProperty()
    # soda2Slider = NumericProperty()

    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        # self.add_widget(TabbedPanelHeader(text='From INIT'))

    # Uses the current liquid amount to get color of slider
    def get_slider_color(self, value):
        if value > 875:
            return (1-((value-875)/875)),1.0,0,1
        elif value <= 875:
            return 1.0,value/875,0,1

    pass

### Mixed Drinks Screen
class MixedDrinksScreen(Screen):

    def __init__(self, **kwargs):
        super(MixedDrinksScreen, self).__init__(**kwargs)
        # self.add_credits_label()
        
    def get_credits(self):
        return "Credits: {0}".format(App.get_running_app().loggedInUserCredits)

    # def add_credits_label(self):
    #     creditsLabel = Label(text=f"Credits: {currentUserCredits}",
    #                         pos_hint ={'right': 1, 'top': .95},
    #                         size_hint=(.35, .18),
    #                         font_name='assets/fonts/Avenir/AvenirNextLTPro-HeavyCn.otf',
    #                         font_size=24,
    #                         text_size=self.size,
    #                         halign='right',
    #                         valign='middle')
    #     self.add_widget(creditsLabel)

    def on_pre_enter(self):
        self.tester()
        self.sm = sm
        # self.screen = self.sm.get_screen('mixedDrinks')
        # mixed_drinks_list = drinks_list["mixed_drinks_list"]
        # DSV = DrinkScrollView()
        # DSV.build_drink_grid_layout(mixed_drinks_list, self.screen.ids.mixed)
        # DrinkScrollView().build_drink_list(mixed_drinks_list, mixed)

    def tester(self):
        if commenting:
            print("Mixed Drinks List:")
            for drink in drink_list["mixed_drinks_list"]:
                print("\tName: {}, Ingredients: {}".format(drink["name"], drink["ingredients"]))
            pass
        pass

    def _do_pour(self, drink_data):
        print("Drink data pressed: {0}".format(drink_data))

    def do_pour(self):
        print("Drink data pressed")


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

### Shots Drinks Screen
class ShotsDrinksScreen(Screen):

    creditsObserver = ObjectProperty()
    shots_list = drinks_list["shots_list"]

    def on_pre_enter(self):
        self.tester()
        self.creditsObserver.text = "Credits: {0}".format(currentUserCredits)
        
    # def get_credits(self):
        # return "Credits: {0}".format(App.get_running_app().loggedInUserCredits)

    # def get_mixed_drinks(self):

    def tester(self):

        if commenting:
            print("Shots List:")
            for drink in drink_list["shots_list"]:
                print("\tName: {}, Ingredients: {}".format(drink["name"], drink["ingredients"]))
            pass

        pass

    pass

### Soda Drinks Screen
class SodaDrinksScreen(Screen):

    soda_list = drinks_list["soda_list"]

    def on_pre_enter(self):
        self.tester()

    # def get_mixed_drinks(self):

    def tester(self):

        if commenting:
            print("Soda List:")
            for drink in drink_list["soda_list"]:
                print("\tName: {}, Ingredients: {}".format(drink["name"], drink["ingredients"]))
            pass

        pass

    pass

# Keyboard Screen
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