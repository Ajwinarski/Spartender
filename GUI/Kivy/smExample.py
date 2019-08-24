import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.settings import Settings
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty

# Set the window color and to fullscreen without the top menu
from kivy.core.window import Window
Window.size = (800, 480)
Window.clearcolor = (0.09411,0.270588,0.231372,1) #rgba(24,69,59,1)
Window.borderless = True

config = ConfigParser()


# Screen Definition
class MainScreen(Screen):
    pass

class DrinksScreen(Screen):
    pass

class ConfigScreen(Screen):
    pass

class SettingsScreen(Screen):
    s = Settings()

    pass

# Screen Manager Definition
class ScreenManagement(ScreenManager):
    pass

# Load the main menu .kv file
presentation = Builder.load_file("spartender.kv")

# Create the screen manager
# sm = ScreenManager()
# sm.add_widget(MainScreen(name='main'))
# sm.add_widget(AnotherScreen(name='other'))

class SpartenderApp(App):
    def build(self):
        return presentation
        #return sm

SpartenderApp().run()
