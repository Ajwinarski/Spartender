import kivy
from kivy import require

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
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
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty

# Imports the json settings
from settingsjson import settings_json
from functools import partial

# Set the window color and to fullscreen without the top menu
from kivy.core.window import Window
Window.size = (800, 480)
Window.clearcolor = (0.09411,0.270588,0.231372,1) #rgba(24,69,59,1) / 255
Window.borderless = True

# Define the config var for settings
config = ConfigParser()

class MyKeyboardListener(Screen):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
                            self._keyboard_close, self, 'text')

        # if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
        vkeyboard = self._keyboard.widget

            # Define the keyboard layout
        vkeyboard.layout = 'numeric.json'
        vkeyboard.size_hint = (.65,.4)
        vkeyboard.pos_hint_x = .5
            # for layout in vkeyboard.available_layouts:
            #     print(layout)

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

class IconButton(ButtonBehavior, Image):

    pass

    # def _keyboard_open(self):
    #     # self._keyboard = Window.request_keyboard(
    #     #                     self._keyboard_close, self, 'text')
    #
    #     if self._keyboard.widget:
    #         # If it exists, this widget is a VKeyboard object which you can use
    #         # to change the keyboard layout.
    #         vkeyboard = self._keyboard.widget
    #
    #         # Define the keyboard layout
    #         vkeyboard.layout = 'numeric.json'
    #         vkeyboard.size_hint = (.65,.4)
    #         # for layout in vkeyboard.available_layouts:
    #         #     print(layout)
    #
    #     self._keyboard.bind(on_key_down=self._on_keyboard_down)
    #     pass

        # if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            # vkeyboard = self._keyboard.widget
            # vkeyboard.layout = 'numeric.json'
            # vkeyboard.layout = 'qwerty'
            # vkeyboard.size_hint_x = .5
            # vkeyboard.size_hint = (.5,.5)
            # vkeyboard.margin_hint = [0,0,0,0]
            # vkeyboard.center_x = 0.5
            # vkeyboard.pos_hint = {'center_x': .5, 'y': 30}
            # vkeyboard.background_color = 255,255,255,0
            # vkeyboard.key_background_color = 0.09411,0.270588,0.231372,1

        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # # vkeyboard = self._keyboard.widget
        # self._keyboard.layout = 'numeric.json'
        # # vkeyboard.size_hint_x = .5
        # self._keyboard.size_hint = (.5,.5)
        # self._keyboard.margin_hint = [0,0,0,0]

    # def _keyboard_close(self):
    #     print('Keyboard closed!')
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None
    #
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     print('The key', keycode, 'has been pressed')
    #     print(' - text is %r' % keycode[1])
    #     print(' - modifiers are %r' % modifiers)
    #
    #     # Keycode is composed of an integer + a string
    #     # If we hit escape, release the keyboard
    #     if keycode[1] == 'escape':
    #         keyboard.release()
    #
    #     # Return True to accept the key. Otherwise, it will be used by
    #     # the system.
    #     return True
    #
    # pass

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

""" Menu Screen Definition """

class MainScreen(Screen):

    settingsImage = ObjectProperty()
    drinksImage = ObjectProperty()
    configImage = ObjectProperty()

    def do_pressed(self, button, imagePath):
        if button == 's': self.settingsImage.source = imagePath
        elif button == 'd': self.drinksImage.source = imagePath
        else: self.configImage.source = imagePath
        # print("Pressed")

    def do_released(self, button, imagePath):
        if button == 's': self.settingsImage.source = imagePath
        elif button == 'd': self.drinksImage.source = imagePath
        else: self.configImage.source = imagePath
        # print("Released")

    pass

class DrinksScreen(Screen):
    pass

class ConfigScreen(Screen):
    pass

class MixedDrinksScreen(Screen):
    pass

class ShotsDrinksScreen(Screen):
    pass

class SodaDrinksScreen(Screen):
    pass

class KeypadPopup(Popup):
    pin1Observer = ObjectProperty()
    pin2Observer = ObjectProperty()
    pin3Observer = ObjectProperty()
    pin4Observer = ObjectProperty()

    pinNums = []

    def do_pin_pressed(self, num):
        self.pinNums.append(num)

        # Add the stars based on how many pins have been entered
        if len(self.pinNums) == 1:
            self.change_text('a', self.pin1Observer)
        elif len(self.pinNums) == 2:
            self.change_text('a', self.pin2Observer)
        elif len(self.pinNums) == 3:
            self.change_text('a', self.pin3Observer)
        elif len(self.pinNums) == 4:
            self.change_text('a', self.pin4Observer)
            self.do_check_pin()

    def change_text(self, func, observer):
        if func == 'a':
            observer.text = '*'
        else:
            observer.text = '____'

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

        pass

    def do_check_pin(self):

        # TODO: Check database for pin numbers

        # Close the Popup
        self.dismiss()

        # Reset the pinNums string
        self.pinNums = []
        self.change_text('d', self.pin1Observer)
        self.change_text('d', self.pin2Observer)
        self.change_text('d', self.pin3Observer)
        self.change_text('d', self.pin4Observer)

        pass


    pass

# Screen Manager Definition
# class ScreenManager(ScreenManager):
#     def __init__(self, **kwargs):
#         return super(ScreenManager, self).__init__(**kwargs)

# Load the main menu .kv file
# presentation = Builder.load_file("spartender.kv")

class SpartenderApp(App):

    screen_names = ListProperty([])
    sm = ScreenManager(transition = SlideTransition(duration = 0.55))
    # keypad_Popup = KeypadPopup()

    # keyboard = Popup(title='Enter Your Pin',
    #     content=Button(text='1'),
    #     size_hint=(None, None), size=(360, 360))

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

        # Add the screen widgets
        # Main screen pages
        self.sm.add_widget(mainPage)
        self.sm.add_widget(drinksPage)
        self.sm.add_widget(configPage)

        # Drinks screen pages
        self.sm.add_widget(mixedDrinksPage)
        self.sm.add_widget(shotsDrinksPage)
        self.sm.add_widget(sodaDrinksPage)

        # Additional screens
        # self.sm.add_widget(keypadPage)

        # Set the first page to be main
        self.sm.current = "main"

        return self.sm

    def hideWidget(self, wid, hide):
        if hide:
            wid.opacity, wid.disabled = 0, True
        elif not hide:
            wid.opacity, wid.disabled = 1, False
        pass

    def build_config(self, config):
        config.setdefaults('settings', {
            'partyMode': False,
            'pinMode': True,
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})

    def build_settings(self, settings):
        settings.add_json_panel('Spartender Settings',
                                self.config,
                                data=settings_json)
        # Use this is modify the settings appearance
        # settings.pos_hint = ({"right": 1, "center_y": .5})
        # settings.size_hint = (0.9, 0.9)

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)

            # Logic for Party Mode
            if token == ('settings', 'partyMode'):
                # Define the screen(s) and button(s) you want to hide
                mainScreen = self.sm.get_screen('main')
                configWid = mainScreen.ids.configBtn
                settingsWid = mainScreen.ids.settingsBtn
                widgets = [configWid, settingsWid]

                # Call the function to hide config button here
                for wid in widgets:
                    self.hideWidget(wid, int(value))

                # Used to check the partyMode value in our .ini file
                # print(config.get('settings', 'partyMode'))

            # Logic for Pin Mode
            elif token == ('settings', 'pinMode'):
                print('Pin mode set to ', value)
                # Keyboard widget definition
                # keyboard = MyKeyboardListener(name='keypad')


                def callMe():
                    print("keyboard closed")
                    pass

                if int(value):
                    # Open the keyboard
                    # keyboard = MyKeyboardListener(name='keyboard')

                    # self.sm.current = 'keypadNums'
                    # keyboard._keyboard_open()
                    # Window.request_keyboard(callMe, self, input_type='tel')
                    # Window.add_widget(MyKeyboardListener(name='keypad'))

                    self.keypadPage.open()

                # if not int(value):
                    # Close the keyboard
                    # keyboard._keyboard_close()
                    # keyboard.unbind(on_key_down=self._on_keyboard_down)
                    # Window.release_all_keyboards()



if __name__ == '__main__':
    SpartenderApp().run()
