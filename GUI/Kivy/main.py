import kivy
from kivy import require

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
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
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            vkeyboard = self._keyboard.widget
            vkeyboard.layout = 'numeric.json'
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

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

""" Screen Definition """
class MainScreen(Screen):
    pass

class DrinksScreen(Screen):
    pass

class ConfigScreen(Screen):
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

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        mainPage = MainScreen(name = "main")
        drinksPage = DrinksScreen(name='drinks')
        configPage = ConfigScreen(name='config')
        # keyboard = MyKeyboardListener(name='keyboard')

        # Create the screen manager
        # self.sm = ScreenManager(transition = SlideTransition(duration = 0.8))
        self.sm.add_widget(mainPage)
        self.sm.add_widget(drinksPage)
        self.sm.add_widget(configPage)

        self.sm.current = "main"

        # self.screens = {}
        # self.available_screens = sorted([
        #     'Homepage', 'Drinks'
        # ])
        # self.screen_names = self.available_screens
        # curdir = dirname(__file__)
        # self.available_screens = [join(curdir, 'screens',
        #     '{}.kv'.format(fn).lower()) for fn in self.available_screens]

        # setting = self.config.get('settings', 'partyMode')
        # return presentation
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

            elif token == ('settings', 'pinMode'):
                print('Pin mode set to ', value)
                keyboard = MyKeyboardListener(name='keyboard')

                if int(value):
                    self.sm.add_widget(keyboard)
                if not int(value):
                    self.sm.remove_widget(keyboard)
                    # keyboard._keyboard_closed()
                    # self.sm.remove_widget(keyboard)



if __name__ == '__main__':
    SpartenderApp().run()
