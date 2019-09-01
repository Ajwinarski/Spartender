import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.settings import Settings
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.factory import Factory
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty

# Imports the json settings
from settingsjson import settings_json

# Set the window color and to fullscreen without the top menu
from kivy.core.window import Window
Window.size = (800, 480)
Window.clearcolor = (0.09411,0.270588,0.231372,1) #rgba(24,69,59,1) / 255
Window.borderless = True


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

    # partyMode = BooleanProperty(False)

    # def hideConfig(self):
    #     if config is self.config:
    #         for item in config.sections():
    #             print(config.options(item))
    #         return False
    pass

class DrinksScreen(Screen):
    pass

class ConfigScreen(Screen):
    pass

# class SettingsScreen(Screen):
#     # s = Settings()
#     pass

# Screen Manager Definition
# class ScreenManager(ScreenManager):
#     def __init__(self, **kwargs):
#         return super(ScreenManager, self).__init__(**kwargs)

# Load the main menu .kv file
# presentation = Builder.load_file("spartender.kv")

# Define the config var for settings
config = ConfigParser()

class SpartenderApp(App):

    screen_names = ListProperty([])
    sm = ScreenManager(transition = SlideTransition(duration = 0.55))

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        mainPage = MainScreen(name = "main")
        drinksPage = DrinksScreen(name='drinks')
        configPage = ConfigScreen(name='config')

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
        settings.pos_hint = ({"right": 1, "center_y": .5})
        settings.size_hint = (0.9, 0.9)

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('settings', 'partyMode'):
                # print('Party mode set to ', value)
                # print(self.sm.screens)
                if value == '1':
                    print("Value is true")
                    self.sm.get_screen('main').ids.configBtn.disabled = True
                    self.sm.get_screen('main').ids.configBtn.size_hint = (0, 0)
                elif value == '0':
                    print("Value is false")
                    self.sm.get_screen('main').ids.configBtn.disabled = False
                    self.sm.get_screen('main').ids.configBtn.size_hint = (.25, .4)

                # print(config.get('settings', 'partyMode'))

                # Call the function to hide config button here

                # self.root.ids.configScreen.ids.configBtn.text = "Test"
                # self.root.ids.configBtn.text = "Worked"
            elif token == ('settings', 'pinMode'):
                print('Pin mode set to ', value)


if __name__ == '__main__':
    SpartenderApp().run()
