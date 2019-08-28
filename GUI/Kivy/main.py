import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.settings import Settings
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

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

config = ConfigParser()


# Screen Definition
class MainScreen(Screen):
    # def hideConfig(self):
    #     self.root.ids.configBtn.disabled = True
    pass

class DrinksScreen(Screen):
    pass

class ConfigScreen(Screen):
    pass

class SettingsScreen(Screen):
    # s = Settings()
    pass

# Screen Manager Definition
class ScreenManager(ScreenManager):
    pass
    # def __init__(self, **kwargs):
    #     super(ScreenManager, self).__init__(**kwargs)
    #     presentation = Builder.load_file("spartender.kv")
    #     return presentation

# Load the main menu .kv file
# presentation = Builder.load_file("spartender.kv")

# Create the screen manager
# sm = ScreenManager()
# sm.add_widget(MainScreen(name='main'))
# sm.add_widget(AnotherScreen(name='other'))

class SpartenderApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        setting = self.config.get('settings', 'partyMode')
        # return presentation
        # return ScreenManager()
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
        settings.pos_hint = ({"right": 1, "center_y": .5})
        settings.size_hint = (0.9, 0.9)

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('settings', 'partyMode'):
                print('Party mode set to ', value)
                # self.root.ids.configScreen.ids.configBtn.text = "Test"
                # self.root.ids.configBtn.text = "Worked"
            elif token == ('settings', 'pinMode'):
                print('Pin mode set to ', value)


if __name__ == '__main__':
    SpartenderApp().run()
