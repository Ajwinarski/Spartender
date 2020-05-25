import kivy
#kivy.require('1.0.7')

from time import time
from os.path import dirname, join

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty


# Set the window to fullscreen without the top menu
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'fake')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
#Config.set('graphics', 'position', 'custom')

class SpartenderScreen(Screen):

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(SpartenderScreen, self).add_widget(*args)

class SpartenderApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'Spartender'
        #Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'Homepage', 'Drinks'
        ])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        #self.load_kv('spartender.kv')
        self.go_next_screen()
        #return root.go_next_screen()
        #self.load_kv('showcase.kv')

        # exitBtn = Button(text="Exit", font_size = 18,
        #                  halign = 'left',
        #                  valign = 'bottom',
        #                  pos_hint={'right':1,'top':1},
        #                  size_hint =(None, None))
        # exitBtn.bind(on_press=exit)
        # return exitBtn
        #return Label(text="Spartender")

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    # def on_current_title(self, instance, value):
    #     self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

# class ImageButton()


SpartenderApp().run()
